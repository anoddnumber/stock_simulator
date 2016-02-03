from pymongo import MongoClient
from py.exceptions.create_account_errors import DuplicateEmailError, DuplicateUsernameError

from user import User
from py.exceptions.invalid_usage import InvalidUsage


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
    def create_user(user):
        print 'createUser'
        userInDB = UsersDbAccess.get_user_by_username(user.username)
        if userInDB is not None:
            print "User already exists. Choose another username."
            raise DuplicateUsernameError('Username already taken.')
        elif UsersDbAccess.get_user_by_email(user.email) is not None:
            print "Account already exists for the given email."
            raise DuplicateEmailError('Account already exists for the given email.')
        else:
            UsersDbAccess.collection.insert_one(user.getDict())
        return "Successful"

    @staticmethod
    def get_user_by_username(username):
        user_dict = UsersDbAccess.collection.find_one({"username": username})
        if user_dict is not None:
            return User(user_dict)
        print 'No user found with username ' + username
        return None

    @staticmethod
    def get_user_by_email(email):
        user_dict = UsersDbAccess.collection.find_one({"email": email})
        if user_dict is not None:
            return User(user_dict)
        print 'No user found with email ' + email
        return None

    @staticmethod
    def addStockToUser(username, symbol, pricePerStock, quantity):
        userDict = UsersDbAccess.collection.find_one({"username": username})
        totalCost = pricePerStock * quantity
        pricePerStock = str(pricePerStock).replace('.', '_')
        try:
            numStocksOwned = userDict['stocks_owned'][symbol][pricePerStock]
        except KeyError, e:
            numStocksOwned = 0
        key = "stocks_owned." + str(symbol) + "." + pricePerStock

        update = {}
        update[key] = int(numStocksOwned) + quantity
        update["cash"] = float(userDict['cash']) - totalCost
        UsersDbAccess.collection.update({"username": username}, {"$set" : update})
        return "success"

    '''
    Sells stocks for a user, starting from the lowest price bought.
    If the user does not have enough stocks, none are sold and an error is returned.
    '''
    @staticmethod
    def sell_stocks_from_user(username, symbol, quantity, cache):
        user_dict = UsersDbAccess.collection.find_one({"username": username})

        try:
            # the information regarding the symbol
            user_stock_symbol_info = user_dict['stocks_owned'][symbol]
        except KeyError, e:
            return "User " + username + " does not own stock with symbol " + symbol

        num_stocks_owned = 0
        for key in user_stock_symbol_info:
            num_stocks_owned += int(user_stock_symbol_info[key])

        if num_stocks_owned < quantity:
            return "User " + username + " does not own enough of " + symbol + "." \
                   + " Trying to sell " + str(quantity) + " but only owns " + str(num_stocks_owned) + "."

        keys_to_remove = []
        # we now know for sure that the user owns enough stock.
        for key in user_stock_symbol_info:
            num_stocks_of_price = int(user_stock_symbol_info[key])
            if num_stocks_of_price >= quantity:
                user_stock_symbol_info[key] = str(num_stocks_of_price - quantity)
                break
            else:
                quantity -= num_stocks_of_price
                keys_to_remove.append(key)

        for key in keys_to_remove:
            user_stock_symbol_info.pop(key, None)

        # remove the stock entry from the stocks_owned if the user has sold all stocks of that symbol
        if not user_stock_symbol_info:
            user_dict['stocks_owned'].pop(symbol, None)

        key = "stocks_owned"
        update = {}
        update[key] = user_dict['stocks_owned']

        update["cash"] = float(user_dict['cash']) + quantity * float(cache.get_stock_price(symbol))
        UsersDbAccess.collection.update({"username": username}, {"$set" : update})
        return "success"
