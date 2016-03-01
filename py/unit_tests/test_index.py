import unittest
from test_client import TestClient
from db_info import DBInfo

collection = DBInfo.get_collection()

class TestIndex(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()

    def tearDown(self):
        collection.remove({"username": TestClient.test_user_name})

    def test_basic(self):
        print "\ntest_basic"
        rv = self.client.get('/')

        #make sure we are on the login page
        assert TestClient.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_logged_in(self):
        print "\ntest_logged_in"
        self.client.create_account()
        self.client.login()
        rv = self.client.get('/')
        assert not TestClient.is_login_page(rv.data)
        assert TestClient.is_redirect(rv.data, '/theApp')

if __name__ == '__main__':
    unittest.main()