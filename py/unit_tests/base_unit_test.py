import unittest
from stock_simulator_test_client import StockSimulatorTestClient
from simulator import stock_user_datastore, db
from test_info import TestInfo
import ast
from py.datastores.transaction_datastore import MongoEngineTransactionDatastore


class BaseUnitTest(unittest.TestCase):
    def setUp(self):
        print "\nSetting up a unit test"
        self.client = StockSimulatorTestClient()
        print "\n"

    def tearDown(self):
        print "Tearing down a unit test"
        user = stock_user_datastore.find_user(username=TestInfo.user_name)
        if user:
            transaction_datastore = MongoEngineTransactionDatastore(db)
            transactions = transaction_datastore.find_transactions(user.get_id())
            for transaction in transactions:
                transaction.delete()
            user.delete()
        print

    def assert_user_info(self, stocks_owned, cash):
        rv = self.client.get('/getUserInfo')
        user_dict = ast.literal_eval(rv.data)

        print "from database - stocks owned: " + str(user_dict.get('stocks_owned'))
        print "from test     - stocks owned: " + str(stocks_owned)
        print "from database - cash: " + str(user_dict.get('cash'))
        print "from test     - cash: " + str(round(cash, 2))

        assert user_dict.get('stocks_owned') == stocks_owned
        assert float(user_dict.get('cash')) == round(cash, 2)

        return user_dict
