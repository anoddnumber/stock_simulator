from pymongo import MongoClient
from user import User
from invalid_usage import InvalidUsage

class DbAccess:
    def __init__(self, dbname):
        self.dbname = dbname
        self.client = MongoClient()
        self.db = self.client[dbname]

class UsersDbAccess:
    dbname = "stock_market_simulator_db"
    client = MongoClient()
    db = client[dbname]
    collectionName = "users"
    collection = db[collectionName]

    @staticmethod
    def createUser(user):
        userInDB = UsersDbAccess.getUserByUsername(user.username)
        if userInDB is not None:
            print "User already exists. Choose another username."
            raise InvalidUsage('Username already taken.', status_code=400)
        else:
            UsersDbAccess.collection.insert_one(user.getDict())
        return "Successful"

    @staticmethod
    def getUserByUsername(username):
        userDict = UsersDbAccess.collection.find_one({"username": username})
        if userDict is not None:
            return User(userDict)
        print 'No user found with username ' + username
        return None

    @staticmethod
    def addStockToUser(username, symbol, pricePerStock, quantity):
        print 'in usersdbaccess'
        userDict = UsersDbAccess.collection.find_one({"username": username})
        print userDict
        totalCost = pricePerStock * quantity
        pricePerStock = str(pricePerStock).replace('.', '_')
        try:
            numStocksOwned = userDict['stocks_owned'][symbol][pricePerStock]
        except KeyError, e:
            numStocksOwned = 0
        key = "stocks_owned." + str(symbol) + "." + pricePerStock
        update = {}
        update[key] = numStocksOwned + quantity
        update["cash"] = float(userDict['cash']) - totalCost
        UsersDbAccess.collection.update({"username": username}, {"$set" : update})
        return "success"
