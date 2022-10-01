from pymongo import MongoClient
import settings as settings

class Database(object):
    ADVERSEA_DATABASE = None
    METRICS_DATABASE = None

    @staticmethod
    def get_database_adversea():
        if Database.ADVERSEA_DATABASE is not None:
            return Database.ADVERSEA_DATABASE

        connection = MongoClient(
            host= settings.MONGO_SERVER_URL + ":" + str(settings.MONGO_SERVER_PORT),
            serverSelectionTimeoutMS = 3000,
            username=settings.MONGO_USER,
            password=settings.MONGO_PASSWORD
        )
        Database.ADVERSEA_DATABASE = connection[settings.MONGO_DB_NAME]

        return Database.ADVERSEA_DATABASE

    @staticmethod
    def get_database_metrics():
        if Database.METRICS_DATABASE is not None:
            return Database.METRICS_DATABASE

        connection = MongoClient(
            host= settings.MONGO_SERVER_URL + ":" + str(settings.MONGO_SERVER_PORT),
            serverSelectionTimeoutMS = 3000,
            username=settings.MONGO_USER,
            password=settings.MONGO_PASSWORD
        )
        Database.METRICS_DATABASE = connection[settings.MONGO_DB_NAME_METRICS]

        return Database.METRICS_DATABASE