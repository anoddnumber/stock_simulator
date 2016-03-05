import unittest
from stock_simulator_test_client import StockSimulatorTestClient
from db_info import DBInfo
from test_info import TestInfo

collection = DBInfo.get_collection()

class TestIndexPage(unittest.TestCase):

    def setUp(self):
        self.client = StockSimulatorTestClient()

    def tearDown(self):
        collection.remove({"username": TestInfo.user_name})

    def test_basic(self):
        print "\ntest_basic"
        rv = self.client.get('/')

        #make sure we are on the login page
        assert StockSimulatorTestClient.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_logged_in(self):
        print "\ntest_logged_in"
        self.client.create_account()
        self.client.login()
        rv = self.client.get('/')
        assert not StockSimulatorTestClient.is_login_page(rv.data)
        assert StockSimulatorTestClient.is_simulator_page(rv.data)

if __name__ == '__main__':
    unittest.main()