import os
import app
import unittest
import tempfile
from pymongo import MongoClient

db_name = "stock_market_simulator_db"
client = MongoClient()
db = client[db_name]
collectionName = "users"
collection = db[collectionName]

test_user_name = "test_user_name"
test_email = "test_email@gmail.com"
test_password = "password"

class TestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.test_app = app.application.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
        collection.remove({"username": test_user_name})

    def login(self, email=test_email, password=test_password):
        return self.test_app.post('/login', data=dict(
            email=email,
            password=password,
        ), follow_redirects=True)

    def create_account(self, email=test_email, username=test_user_name, password=test_password, retype_password=test_password):
        return self.test_app.post('/createAccount', data=dict(
            email=email,
            username=username,
            password=password,
            retypePassword=retype_password,
        ), follow_redirects=True)

    def is_login_page(self, data):
        return 'forgotPasswordLink' in data and 'loginDiv' in data and '<div id="stock_simulator">' not in data

    def is_simulator_page(self, data):
        return '<div id="stock_simulator">' in data

    def test_empty_db(self):
        print "\ntest_empty_db"
        rv = self.test_app.get('/')

        #make sure we are on the login page
        assert self.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_login_success(self):
        print "\ntest_login_success"
        self.create_account()
        rv = self.login()
        assert not self.is_login_page(rv.data)
        assert self.is_simulator_page(rv.data)
        assert rv.status_code == 200

    def test_login_fail(self):
        print "\ntest_login_fail"
        rv = self.login()
        assert 'Email and password do not match up' in rv.data
        assert rv.status_code == 200

    def test_create_account_success(self):
        print "\ntest_create_account_success"
        rv = self.create_account()

        assert self.is_simulator_page(rv.data)
        assert rv.status_code == 200

    def test_create_account_fail(self):
        print "\ntest_create_account_fail"
        rv = self.create_account(retype_password="not_the_same_password")

        assert self.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_duplicate_create_account(self):
        print "\ntest_duplicate_create_account"
        rv = self.create_account()

        assert '<div id="stock_simulator">' in rv.data
        assert rv.status_code == 200

        rv = self.create_account()

        assert self.is_login_page(rv.data)
        assert rv.status_code == 200

if __name__ == '__main__':
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.init_logger()
    app.init_cache('./static/cache.json')
    app.init_db()
    unittest.main()