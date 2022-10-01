from concurrent.futures import ThreadPoolExecutor
import requests
import settings as settings
from db_connector import Database
from requests.packages import urllib3
from datetime import datetime
import time

class Counter:
    executor = ThreadPoolExecutor(max_workers=1)
    # represents, worker. If None, job can be executed, else job is already running. static variable
    WORKER = None
    # is used to check if job has just finished or no job was launched at all
    JUST_FINISHED_FLAG = False

    # return vals:
    # 0: started job
    # 1: job is running
    # 2: job finished
    @staticmethod
    def run_recount():
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if Counter.WORKER is not None:
            if Counter.WORKER.done() and Counter.WORKER.exception() is not None:
                raise Counter.WORKER.exception()
            return 1
        if Counter.WORKER is None and Counter.JUST_FINISHED_FLAG:
            Counter.JUST_FINISHED_FLAG = False
            return 2
        if Counter.WORKER is None and not Counter.JUST_FINISHED_FLAG:
            Counter.WORKER = Counter.executor.submit(Counter.__run_worker)
            return 0
    
    def __run_worker():
        start_time = time.time()
        result = {}
        print("Starting elastic count..")
        result["elastic"] = Counter.__count_elastic()
        print("Elastic done.")
        print("Starting mongo count..")
        result["mongo"] = Counter.__count_mongo()
        print("Mongo done.")
        end_time = time.time()
        result["duration_seconds"] = int(end_time - start_time)
        result["timestamp"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        db_metrics = Database.get_database_metrics()
        db_metrics["articles_summary"].drop()
        print("Writing info to db")
        db_metrics["articles_summary"].insert_one(result)
        # set this to none so another recount can be launched
        print("Reseting flags")
        Counter.WORKER = None
        Counter.JUST_FINISHED_FLAG = True
        print("Recount done.")

    def __count_mongo():
        result = {"regions": {}, "languages": {}, "db_size_bytes": 0, "total_count": 0}
        db_adversea = Database.get_database_adversea()
        f = open("./targets/scraping/config/locale.txt", "r")
        for line in f:
            language, region = line.rstrip().split("-")
            lang_count = db_adversea["articles"].count_documents({"language": language})
            reg_count = db_adversea["articles"].count_documents({"region": region})
            result["languages"][language] = lang_count
            result["regions"][region] = reg_count
        all_articles_count = db_adversea["articles"].count_documents({})
        size = db_adversea.command("dbstats")["dataSize"]
        result["total_count"] = all_articles_count
        result["db_size_bytes"] = size
        return result


    def __count_elastic():
        result = {"regions": {}, "languages": {}, "index_size_bytes": 0, "total_count": 0}
        es_url = "{protocol}://{host}:{port}/{index}/".format(
            protocol=settings.ES_PROTOCOL,
            host=settings.ES_HOST,
            port=settings.ES_PORT,
            index=settings.ELASTIC_INDEX_NAME)
        f = open("./targets/scraping/config/locale.txt", "r")
        # count regions and languages
        for line in f:
            language, region = line.rstrip().split("-")
            lang_count = requests.get(es_url + "_count?q=language:" + language, verify=False, auth=(settings.ES_USER, settings.ES_PASSWORD)).json()["count"]
            result["languages"][language] = lang_count
            reg_count = requests.get(es_url + "_count?q=region:" + region, verify=False, auth=(settings.ES_USER, settings.ES_PASSWORD)).json()["count"]
            result["regions"][region] = reg_count
        # count total number + size
        num_of_articles = requests.get(es_url + "_count", verify=False, auth=(settings.ES_USER, settings.ES_PASSWORD)).json()["count"]
        index_size = requests.get(es_url + "_stats/store", verify=False, auth=(settings.ES_USER, settings.ES_PASSWORD)).json()["_all"]["total"]["store"]["size_in_bytes"]
        result["total_count"] = num_of_articles
        result["index_size_bytes"] = index_size
        return result