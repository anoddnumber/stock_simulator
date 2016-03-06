import unittest
from stock_simulator_test_client import StockSimulatorTestClient
from db_info import DBInfo
from flask import session
from test_info import TestInfo

collection = DBInfo.get_collection()

class TestCase(unittest.TestCase):

    def setUp(self):
        self.client = StockSimulatorTestClient()

    def tearDown(self):
        collection.remove({"username": TestInfo.user_name})

    def test_logout_without_login(self):
        print "\ntest_logout_without_login"

        rv = self.client.logout()
        assert not StockSimulatorTestClient.is_simulator_page(rv.data)
        assert StockSimulatorTestClient.is_login_page(rv.data)

    def test_basic_logout(self):
        print "\ntest_logout"
        self.client.create_account()
        rv = self.client.login()
        assert StockSimulatorTestClient.is_simulator_page(rv.data)

        rv = self.client.logout()
        assert not StockSimulatorTestClient.is_simulator_page(rv.data)
        assert StockSimulatorTestClient.is_login_page(rv.data)
        assert not StockSimulatorTestClient.is_cookie_set(rv.headers)

    def test_logout_session(self):
        print "\ntest_logout_session"
        with self.client as c:
            c.create_account()
            assert str(session.get('username')) == TestInfo.user_name
            c.logout()
            assert session.get('username') is None

if __name__ == '__main__':
    unittest.main()