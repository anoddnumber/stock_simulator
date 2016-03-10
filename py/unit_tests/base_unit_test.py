import unittest
from stock_simulator_test_client import StockSimulatorTestClient
from db_info import DBInfo
from test_info import TestInfo
import ast

collection = DBInfo.get_collection()

class BaseUnitTest(unittest.TestCase):
    def setUp(self):
        print "\nSetting up a unit test"
        self.client = StockSimulatorTestClient()
        print "\n"

    def tearDown(self):
        print "Tearing down a unit test"
        collection.remove({"username": TestInfo.user_name})
        print

    def assert_user_info(self, stocks_owned, cash):
        rv = self.client.get('/getUserInfo')
        user_dict = ast.literal_eval(rv.data)

        print "expect stocks owned to be " + str(user_dict.get('stocks_owned'))

        assert user_dict.get('stocks_owned') == stocks_owned
        assert float(user_dict.get('cash')) == round(cash, 2)

        return user_dict