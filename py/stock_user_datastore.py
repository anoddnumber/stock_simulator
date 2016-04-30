from flask_security import MongoEngineUserDatastore
import logging


class MongoEngineStockUserDatastore(MongoEngineUserDatastore):

    def __init__(self, db, user_model, role_model):
        self.logger = logging.getLogger(__name__)
        MongoEngineUserDatastore.__init__(self, db, user_model, role_model)

    def add_stock_to_user(self, username, symbol, price_per_stock, quantity):
        self.logger.info("Adding stock to user with username " + str(username))
        self.logger.info("Symbol: " + str(symbol) + "\n" +
                         "Price per stock: " + str(price_per_stock) + "\n" +
                         "Quantity: " + str(quantity))

        user = self.find_user(username=username)
        print "user" + str(type(user))
        # user_dict = self.collection.find_one({"username": username})
        total_cost = price_per_stock * quantity

        # format the price_per_stock to always have exactly 2 digits after the decimal
        price_per_stock = '{0:.2f}'.format(price_per_stock)

        # mongodb does not allow periods/has problems with them. Replace them with underscores
        price_per_stock = str(price_per_stock).replace('.', '_')

        try:
            num_stocks_owned_at_price = user['stocks_owned'][symbol][price_per_stock]
        except KeyError, e:
            num_stocks_owned_at_price = 0

        try:
            total_num_stocks_owned = user['stocks_owned'][symbol]['total']
        except KeyError, e:
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
        return "Success"