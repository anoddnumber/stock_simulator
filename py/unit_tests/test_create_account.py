import unittest
from stock_simulator_test_client import StockSimulatorTestClient
from base_unit_test import BaseUnitTest


class TestCreateAccount(BaseUnitTest):

    def test_create_account_success(self):
        print "test_create_account_success"
        rv = self.client.create_account()

        assert StockSimulatorTestClient.is_post_create_account_page(rv.data)
        assert rv.status_code == 200

    def test_different_retype_password(self):
        print "test_different_retype_password"
        rv = self.client.create_account(retype_password="not_the_same_password")

        assert StockSimulatorTestClient.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_duplicate_create_account(self):
        print "test_duplicate_create_account"
        rv = self.client.create_account()

        assert StockSimulatorTestClient.is_post_create_account_page(rv.data)
        assert rv.status_code == 200

        rv = self.client.create_account()

        assert StockSimulatorTestClient.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_create_account_with_username_only_spaces(self):
        print "test_create_account_with_empty_password"
        # self.client.create_account()

        # same email, different username, different password
        rv = self.client.create_account(username="  ")

        assert StockSimulatorTestClient.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_create_account_with_space_in_username(self):
        print "test_create_account_with_space_in_username"
        rv = self.client.create_account(username="test test")

        assert "Username cannot contain spaces" in rv.data
        assert StockSimulatorTestClient.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_duplicate_email(self):
        print "test_duplicate_email"
        self.client.create_account()

        # same email, different username, different password
        rv = self.client.create_account(username="different_username", password="different_pass",
                                        retype_password="different_pass")

        assert "is already associated with an account" in rv.data
        assert StockSimulatorTestClient.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_duplicate_username(self):
        print "test_duplicate_username"
        self.client.create_account()

        # same username, different email, same password
        rv = self.client.create_account(email="different_email@email.com")

        assert "Username already taken" in rv.data
        assert StockSimulatorTestClient.is_login_page(rv.data)
        assert rv.status_code == 200

if __name__ == '__main__':
    unittest.main()