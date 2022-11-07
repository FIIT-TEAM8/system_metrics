from flask import Blueprint, request
from .recount import Counter
from db_connector import Database


scraping_route = Blueprint("scraping", __name__, url_prefix="/scraping")

@scraping_route.route("/recount")
def recount():
    flag = Counter.run_recount()
    if flag == 0:
        return "Recount started", 202
    if flag == 1:
        return "Recount still running", 202
    if flag == 2:
        return "Recount finished!", 200
    
    else:
        return "Finished with exception :(", 500

@scraping_route.route("/daily", methods=["POST"])
def update_daily():
    new = request.get_json()
    scraping_date = new["scraping_date"].split(",")[0]
    db = Database.get_database_metrics()
    if db["daily_stats"].count_documents({"date": scraping_date}) == 0:
        db["daily_stats"].insert_one({
            "date": scraping_date,
            "daily_total_elastic": 0,
            "daily_total_mongo": 0,
            "daily_total_seconds": 0,
            "locales": []
        })
    old = db["daily_stats"].find_one({"date": scraping_date})
    old["locales"].append(new)
    db["daily_stats"].update_one({"date": scraping_date}, {"$set":{
        "daily_total_elastic": old["daily_total_elastic"] + new["elastic_inserts"],
        "daily_total_mongo": old["daily_total_mongo"] + new["mongo_inserts"],
        "daily_total_seconds": old["daily_total_seconds"] + new["elapsed_time_seconds"],
        "locales": old["locales"]
    }})
    
    return "Created", 201



