from pymongo import MongoClient

class DBInfo:
    db_name = "stock_market_simulator_db"
    collection_name = "users"

    @staticmethod
    def get_collection():
        client = MongoClient()
        db = client[DBInfo.db_name]
        collection = db[DBInfo.collection_name]
        return collection