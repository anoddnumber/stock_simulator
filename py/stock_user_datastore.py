from flask_security import MongoEngineUserDatastore
from bson.objectid import ObjectId
import logging


class MongoEngineStockUserDatastore(MongoEngineUserDatastore):

    def __init__(self, db, user_model, role_model):
        super(MongoEngineStockUserDatastore, self).__init__(db, user_model, role_model)
        self.logger = logging.getLogger(__name__)

    def get_user_by_id(self, user_id):
        return self.get_user(ObjectId(user_id))

    # don't call this create_user since it is a parent method
    def create_user_from_user_obj(self, user):
        return self.create_user(email=user.email, username=user.username, password=user.password)

    def get_user_by_username(self, username):
        return self.find_user(username=username)

    def get_user_by_email(self, email):
        return self.find_user(email=email)

    def add_stock_to_user(self, username, symbol, price_per_stock, quantity):
        from simulator import config

        self.logger.info("Adding stock to user with username " + str(username))
        self.logger.info("Symbol: " + str(symbol) + "\n" +
                         "Price per stock: " + str(price_per_stock) + "\n" +
                         "Quantity: " + str(quantity))

        user = self.find_user(username=username)
        total_cost = price_per_stock * quantity + config['commission']

        # format the price_per_stock to always have exactly 2 digits after the decimal
        price_per_stock = '{0:.2f}'.format(price_per_stock)

        # mongodb does not allow periods/has problems with them. Replace them with underscores
        price_per_stock = str(price_per_stock).replace('.', '_')

        try:
            num_stocks_owned_at_price = user['stocks_owned'][symbol][price_per_stock]
        except KeyError:
            num_stocks_owned_at_price = 0

        try:
            total_num_stocks_owned = user['stocks_owned'][symbol]['total']
        except KeyError:
            total_num_stocks_owned = 0

        self.logger.info(str(username) + " already owns " + str(num_stocks_owned_at_price) + " of " + str(symbol) +
                         " at price " + str(price_per_stock))

        updated_quantity = total_num_stocks_owned + quantity
        if not user.stocks_owned.get(symbol):
            user.stocks_owned[symbol] = {}

        user.stocks_owned[symbol][price_per_stock] = updated_quantity
        user.stocks_owned[symbol]['total'] = total_num_stocks_owned + quantity
        user.cash = round(float(user['cash']) - total_cost, 2)

        user.save()
        return {"data": user, "error": False}

    def sell_stocks_from_user(self, username, symbol, quantity, cache):
        """"
        Sells stocks for a user, starting from the lowest price bought.
        If the user does not have enough stocks, none are sold and an error is returned.
        """
        # user_dict = self.collection.find_one({"username": username})
        user = self.find_user(username=username)
        self.logger.info("Selling stocks from user with username " + str(username))
        self.logger.info("Symbol: " + str(symbol) + "\n" +
                         "Quantity: " + str(quantity))

        try:
            # the information regarding the symbol
            user_stock_symbol_info = user['stocks_owned'][symbol]
        except KeyError, e:
            self.logger.exception("User " + str(username) + " does not own stock with symbol " + str(symbol))
            return {"data": "User does not own stock", "error": True}

        user_stock_symbol_info.pop('total', None)  # remove the total and add it back at the end
        # TODO: use the total quantity field
        num_stocks_owned = 0
        for key in user_stock_symbol_info:
            num_stocks_owned += int(user_stock_symbol_info[key])

        if num_stocks_owned < quantity:
            self.logger.warning("User " + str(username) + " does not own enough of " + str(symbol) + "." +
                                " Trying to sell " + str(quantity) + " but only owns " + str(num_stocks_owned) + ".")
            return {"data": "User does not own enough stock", "error": True}

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
            user.stocks_owned.pop(symbol, None)
        else:
            # otherwise update the total field
            user['stocks_owned'][symbol]['total'] = num_stocks_owned - quantity

        user.cash = round(float(user['cash']) + quantity * float(cache.get_stock_price(symbol)), 2)
        user.save()

        self.logger.info("Updating the database for a sell transaction for username " + username)
        self.logger.info("Stock(s) sold successfully")

        return {"data": user, "error": False}
