import unittest
from stock_simulator_test_client import StockSimulatorTestClient
from db_info import DBInfo
from test_info import TestInfo

collection = DBInfo.get_collection()

class BaseUnitTest(unittest.TestCase):
    def setUp(self):
        print "Setting up a unit test"
        self.client = StockSimulatorTestClient()
        print "\n"

    def tearDown(self):
        print "Tearing down a unit test"
        collection.remove({"username": TestInfo.user_name})
        print "\n"