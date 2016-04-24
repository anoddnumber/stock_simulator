import unittest
from stock_simulator_test_client import StockSimulatorTestClient
from flask import session
from test_info import TestInfo
from base_unit_test import BaseUnitTest

class TestLogout(BaseUnitTest):

    def test_logout_without_login(self):
        print "test_logout_without_login"

        rv = self.client.logout()
        # print "rv.data: " + str(rv.data)
        assert not StockSimulatorTestClient.is_simulator_page(rv.data)
        assert StockSimulatorTestClient.is_login_page(rv.data)

    def test_basic_logout(self):
        print "test_logout"
        self.client.create_account()
        self.client.confirm_test_account()
        rv = self.client.login()
        assert StockSimulatorTestClient.is_simulator_page(rv.data)

        rv = self.client.logout()
        assert not StockSimulatorTestClient.is_simulator_page(rv.data)
        assert StockSimulatorTestClient.is_login_page(rv.data)

    def test_logout_session(self):
        print "test_logout_session"
        with self.client as c:
            c.create_account()
            c.logout()

if __name__ == '__main__':
    unittest.main()