import unittest
from pymongo import MongoClient
from test_client import TestClient

db_name = "stock_market_simulator_db"
client = MongoClient()
db = client[db_name]
collectionName = "users"
collection = db[collectionName]

class TestCase(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()

    def tearDown(self):
        collection.remove({"username": TestClient.test_user_name})

    def test_empty_db(self):
        print "\ntest_empty_db"
        rv = self.client.get('/')

        #make sure we are on the login page
        assert TestClient.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_login_success(self):
        print "\ntest_login_success"
        self.client.create_account()
        rv = self.client.login()
        assert not TestClient.is_login_page(rv.data)
        assert TestClient.is_simulator_page(rv.data)
        assert rv.status_code == 200

    def test_login_fail(self):
        print "\ntest_login_fail"
        rv = self.client.login()
        assert 'Email and password do not match up' in rv.data
        assert rv.status_code == 200

    def test_create_account_success(self):
        print "\ntest_create_account_success"
        rv = self.client.create_account()

        assert TestClient.is_simulator_page(rv.data)
        assert rv.status_code == 200

    def test_create_account_fail(self):
        print "\ntest_create_account_fail"
        rv = self.client.create_account(retype_password="not_the_same_password")

        assert TestClient.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_duplicate_create_account(self):
        print "\ntest_duplicate_create_account"
        rv = self.client.create_account()

        assert TestClient.is_simulator_page(rv.data)
        assert rv.status_code == 200

        rv = self.client.create_account()

        assert TestClient.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_logout(self):
        #TODO
        pass

if __name__ == '__main__':
    unittest.main()