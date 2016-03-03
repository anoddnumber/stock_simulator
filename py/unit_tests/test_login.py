import unittest
from test_client import TestClient
from db_info import DBInfo

collection = DBInfo.get_collection()

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()

    def tearDown(self):
        collection.remove({"username": TestClient.test_user_name})

    def test_login_success(self):
        print "\ntest_login_success"
        self.client.create_account()
        rv = self.client.login()
        assert not TestClient.is_login_page(rv.data)
        assert TestClient.is_simulator_page(rv.data)
        assert rv.status_code == 200

    def test_login_without_account(self):
        print "\ntest_login_without_account"
        rv = self.client.login()
        assert 'Email and password do not match up' in rv.data
        assert rv.status_code == 200

    def test_login_bad_password(self):
        print "\ntest_login_bad_password"
        self.client.create_account()
        rv = self.client.login(password="bad_password")
        assert TestClient.is_login_page(rv.data)
        assert not TestClient.is_simulator_page(rv.data)
        assert rv.status_code == 200

    def test_login_nonexistent_email(self):
        print "\ntest_login_nonexistent_email"
        rv = self.client.login('email_that_does_not_exist@asdf.fake')
        assert 'Email and password do not match up' in rv.data
        assert rv.status_code == 200

if __name__ == '__main__':
    unittest.main()