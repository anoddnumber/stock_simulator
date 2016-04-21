import unittest
from stock_simulator_test_client import StockSimulatorTestClient
from base_unit_test import BaseUnitTest
from simulator import app


class TestLogin(BaseUnitTest):

    def test_login_success(self):
        print "test_login_success"
        self.client.create_account()

        self.client.confirm_test_account()
        rv = self.client.login()

        assert not StockSimulatorTestClient.is_login_page(rv.data)
        assert StockSimulatorTestClient.is_simulator_page(rv.data)
        assert rv.status_code == 200

    def test_login_without_account(self):
        print "test_login_without_account"
        rv = self.client.login()

        assert app.config.get('SECURITY_MSG_USER_DOES_NOT_EXIST')[0] in rv.data
        assert not StockSimulatorTestClient.is_simulator_page(rv.data)
        assert rv.status_code == 200

    def test_login_bad_password(self):
        print "test_login_bad_password"
        self.client.create_account()
        rv = self.client.login(password="bad_password")

        assert app.config.get('SECURITY_MSG_INVALID_PASSWORD')[0] in rv.data
        assert not StockSimulatorTestClient.is_simulator_page(rv.data)
        assert rv.status_code == 200

    def test_login_nonexistent_email(self):
        print "test_login_nonexistent_email"
        rv = self.client.login('email_that_does_not_exist@asdf.fake')

        assert app.config.get('SECURITY_MSG_USER_DOES_NOT_EXIST')[0] in rv.data
        assert not StockSimulatorTestClient.is_simulator_page(rv.data)
        assert rv.status_code == 200

    def test_unconfirmed_account(self):
        print "test_unconfirmed_account"
        self.client.create_account()
        rv = self.client.login()

        assert app.config.get('SECURITY_MSG_CONFIRMATION_REQUIRED')[0] in rv.data
        assert not StockSimulatorTestClient.is_simulator_page(rv.data)
        assert rv.status_code == 200

if __name__ == '__main__':
    unittest.main()