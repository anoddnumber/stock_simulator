import unittest
from test_client import TestClient
from db_info import DBInfo
from flask import Flask, session

collection = DBInfo.get_collection()

class TestCase(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()

    def tearDown(self):
        collection.remove({"username": TestClient.test_user_name})

    def test_basic_logout(self):
        print "\ntest_logout"
        self.client.create_account()
        rv = self.client.login()
        assert TestClient.is_simulator_page(rv.data)

        rv = self.client.logout()
        assert not TestClient.is_simulator_page(rv.data)
        assert TestClient.is_login_page(rv.data)


if __name__ == '__main__':
    unittest.main()