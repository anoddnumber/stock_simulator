import unittest
from stock_simulator_test_client import StockSimulatorTestClient
from db_info import DBInfo
from test_info import TestInfo

collection = DBInfo.get_collection()

class TestCreateAccount(unittest.TestCase):

    def setUp(self):
        self.client = StockSimulatorTestClient()

    def tearDown(self):
        collection.remove({"username": TestInfo.user_name})

    def test_create_account_success(self):
        print "\ntest_create_account_success"
        rv = self.client.create_account()

        assert StockSimulatorTestClient.is_simulator_page(rv.data)
        assert rv.status_code == 200

    def test_different_retype_password(self):
        print "\ntest_different_retype_password"
        rv = self.client.create_account(retype_password="not_the_same_password")

        assert StockSimulatorTestClient.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_duplicate_create_account(self):
        print "\ntest_duplicate_create_account"
        rv = self.client.create_account()

        assert StockSimulatorTestClient.is_simulator_page(rv.data)
        assert rv.status_code == 200

        rv = self.client.create_account()

        assert StockSimulatorTestClient.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_same_username(self):
        print "\ntest_same_username"
        self.client.create_account()

        #same email, different username, different password
        rv = self.client.create_account(username="different_username", password="different_pass", retype_password="different_pass")

        assert "Email already taken." in rv.data
        assert StockSimulatorTestClient.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_same_email(self):
        print "\ntest_same_email"
        self.client.create_account()

        #same username, different email, same password
        rv = self.client.create_account(email="different_email@email.com")

        assert "Username already taken." in rv.data
        assert StockSimulatorTestClient.is_login_page(rv.data)
        assert rv.status_code == 200

if __name__ == '__main__':
    unittest.main()