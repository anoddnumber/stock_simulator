import unittest
from test_client import TestClient
from db_info import DBInfo

collection = DBInfo.get_collection()

class TestCreateAccount(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()

    def tearDown(self):
        collection.remove({"username": TestClient.test_user_name})

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

if __name__ == '__main__':
    unittest.main()