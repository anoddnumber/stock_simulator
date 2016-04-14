import unittest
from stock_simulator_test_client import StockSimulatorTestClient
from base_unit_test import BaseUnitTest

class TestLogin(BaseUnitTest):

    def test_login_success(self):
        print "test_login_success"
        self.client.create_account()
        self.client.logout()
        rv = self.client.login()

        assert not StockSimulatorTestClient.is_login_page(rv.data)
        assert StockSimulatorTestClient.is_simulator_page(rv.data)
        assert rv.status_code == 200

    def test_login_without_account(self):
        print "test_login_without_account"
        rv = self.client.login()
        assert 'Email and password do not match up' in rv.data
        assert rv.status_code == 200

    def test_login_bad_password(self):
        print "test_login_bad_password"
        self.client.create_account()
        self.client.logout()
        rv = self.client.login(password="bad_password")
        assert StockSimulatorTestClient.is_login_page(rv.data)
        assert not StockSimulatorTestClient.is_simulator_page(rv.data)
        assert rv.status_code == 200

    def test_login_nonexistent_email(self):
        print "test_login_nonexistent_email"
        rv = self.client.login('email_that_does_not_exist@asdf.fake')
        assert 'Email and password do not match up' in rv.data
        assert rv.status_code == 200

if __name__ == '__main__':
    unittest.main()