import unittest
from stock_simulator_test_client import StockSimulatorTestClient
from base_unit_test import BaseUnitTest


class TestIndexPage(BaseUnitTest):

    def test_basic(self):
        print "test_basic"
        rv = self.client.get('/')

        # make sure we are on the login page
        assert StockSimulatorTestClient.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_logged_in(self):
        print "test_logged_in"
        self.client.create_account()
        self.client.confirm_test_account()
        self.client.login()
        rv = self.client.get('/')
        assert not StockSimulatorTestClient.is_login_page(rv.data)
        assert StockSimulatorTestClient.is_simulator_page(rv.data)

if __name__ == '__main__':
    unittest.main()