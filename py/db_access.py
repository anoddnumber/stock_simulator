from pymongo import MongoClient
from bson.objectid import ObjectId

# from user import User
from db_info import DBInfo
import logging

class DbAccess:
    def __init__(self, dbname):
        self.dbname = dbname
        self.client = MongoClient()
        self.db = self.client[dbname]

class UsersDbAccess:

    collection = DBInfo.get_collection()

    def __init__(self, user_datastore):
        self.logger = logging.getLogger(__name__)
        self.user_datastore = user_datastore

    def get_user_by_id(self, user_id):
        return self.user_datastore.get_user(ObjectId(user_id))

    def create_user(self, user):
        return self.user_datastore.create_user(email=user.email, username=user.username, password=user.password)

    def get_user_by_username(self, username):
        return self.user_datastore.find_user(username=username)

    def get_user_by_email2(self, email):
        return self.user_datastore.find_user(email=email)

    def add_stock_to_user(self, username, symbol, price_per_stock, quantity):
        self.logger.info("Adding stock to user with username " + str(username))
        self.logger.info("Symbol: " + str(symbol) + "\n" +
                         "Price per stock: " + str(price_per_stock) + "\n" +
                         "Quantity: " + str(quantity))

        user_dict = UsersDbAccess.collection.find_one({"username": username})
        total_cost = price_per_stock * quantity
        price_per_stock = str(price_per_stock).replace('.', '_')
        try:
            num_stocks_owned = user_dict['stocks_owned'][symbol][price_per_stock]
        except KeyError, e:
            num_stocks_owned = 0
        self.logger.info(str(username) + " already owns " + str(num_stocks_owned) + " of " + str(symbol) +
                         " at price " + str(price_per_stock))
        key = "stocks_owned." + str(symbol) + "." + price_per_stock

        update = {}
        update[key] = int(num_stocks_owned) + quantity
        update["cash"] = round(float(user_dict['cash']) - total_cost, 2)

        self.logger.info("Updating the database for a buy transaction for username " + username)
        self.logger.info("update: " + str(update))

        UsersDbAccess.collection.update({"username": username}, {"$set" : update})

        self.logger.info("Stock(s) bought successfully")
        return "Success"

    '''
    Sells stocks for a user, starting from the lowest price bought.
    If the user does not have enough stocks, none are sold and an error is returned.
    '''
    def sell_stocks_from_user(self, username, symbol, quantity, cache):
        user_dict = UsersDbAccess.collection.find_one({"username": username})
        self.logger.info("Selling stocks from user with username " + str(username))
        self.logger.info("Symbol: " + str(symbol) + "\n" +
                         "Quantity: " + str(quantity))

        try:
            # the information regarding the symbol
            user_stock_symbol_info = user_dict['stocks_owned'][symbol]
        except KeyError, e:
            self.logger.exception("User " + str(username) + " does not own stock with symbol " + str(symbol))
            return "User does not own stock"

        num_stocks_owned = 0
        for key in user_stock_symbol_info:
            num_stocks_owned += int(user_stock_symbol_info[key])

        if num_stocks_owned < quantity:
            self.logger.warning("User " + str(username) + " does not own enough of " + str(symbol) + "." \
                   + " Trying to sell " + str(quantity) + " but only owns " + str(num_stocks_owned) + ".")
            return "User down not enough stock"

        quantity_left = quantity
        keys_to_remove = []
        # we now know for sure that the user owns enough stock.
        for key in user_stock_symbol_info:
            num_stocks_of_price = int(user_stock_symbol_info[key])
            if num_stocks_of_price > quantity_left:
                user_stock_symbol_info[key] = num_stocks_of_price - quantity_left
                break
            else:
                quantity_left -= num_stocks_of_price
                keys_to_remove.append(key)

        for key in keys_to_remove:
            user_stock_symbol_info.pop(key, None)

        # remove the stock entry from the stocks_owned if the user has sold all stocks of that symbol
        if not user_stock_symbol_info:
            user_dict['stocks_owned'].pop(symbol, None)

        key = "stocks_owned"
        update = {}
        update[key] = user_dict['stocks_owned']

        update["cash"] = round(float(user_dict['cash']) + quantity * float(cache.get_stock_price(symbol)), 2)

        self.logger.info("Updating the database for a sell transaction for username " + username)
        self.logger.info("update: " + str(update))

        UsersDbAccess.collection.update({"username": username}, {"$set" : update})

        self.logger.info("Stock(s) sold successfully")
        return "Success"
