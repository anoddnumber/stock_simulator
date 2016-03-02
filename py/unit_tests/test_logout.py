import unittest
from test_client import TestClient
from db_info import DBInfo

collection = DBInfo.get_collection()

class TestCase(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()

    def tearDown(self):
        collection.remove({"username": TestClient.test_user_name})

    def test_logout_without_login(self):
        print "\ntest_logout_without_login"

        rv = self.client.logout()
        assert not TestClient.is_simulator_page(rv.data)
        assert TestClient.is_login_page(rv.data)

    def test_basic_logout(self):
        print "\ntest_logout"
        self.client.create_account()
        rv = self.client.login()
        assert TestClient.is_simulator_page(rv.data)

        rv = self.client.logout()
        assert not TestClient.is_simulator_page(rv.data)
        assert TestClient.is_login_page(rv.data)
        assert not TestClient.is_cookie_set(rv.headers)

if __name__ == '__main__':
    unittest.main()