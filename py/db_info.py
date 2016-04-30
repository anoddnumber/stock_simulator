from pymongo import MongoClient
from simulator import app

class DBInfo:
    db_name = "stock_market_simulator_db"
    # collection_name = "users"
    collection_name = "user"
    db_port = 27017

    @staticmethod
    def get_collection():
        client = MongoClient()
        db_name = app.config['MONGODB_DB']
        db = client[db_name]
        collection = db[DBInfo.collection_name]
        return collection