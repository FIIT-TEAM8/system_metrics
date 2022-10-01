import os


MONGO_SERVER_URL = str(os.environ['MONGO_SERVER_URL'] or 'localhost')
MONGO_SERVER_PORT = str(os.environ['MONGO_SERVER_PORT'] or 27017)
MONGO_USER = str(os.environ['MONGO_USER'] or 'root')
MONGO_PASSWORD = str(os.environ['MONGO_PASSWORD'] or 'password')
# articles db
MONGO_DB_NAME_ARTICLES = str(os.environ['MONGO_DB_NAME_ARTICLES'] or 'system_metrics')
# metrics db
MONGO_DB_NAME_METRICS = str(os.environ['MONGO_DB_NAME_METRICS'] or 'system_metrics')


ES_HOST = str(os.environ['ES_HOST'] or 'localhost')
ES_PORT = str(os.environ['ES_PORT'] or 9200)
ES_USER = str(os.environ['ES_USER'] or 'root')
ES_PASSWORD = str(os.environ['ES_PASSWORD'] or '123')
ELASTIC_INDEX_NAME = str(os.environ['ELASTIC_INDEX_NAME'] or 'main')
ES_PROTOCOL="https"