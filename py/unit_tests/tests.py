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

class TestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.test_app = app.application.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
        collection.remove({"username": "test_user_name"})

    def login(self, email, password):
        return self.test_app.post('/login', data=dict(
            email=email,
            password=password,
        ), follow_redirects=True)

    def create_account(self, email, username, password, retype_password):
        return self.test_app.post('/createAccount', data=dict(
            email=email,
            username=username,
            password=password,
            retypePassword=retype_password,
        ), follow_redirects=True)

    def is_login_page(self, data):
        return 'forgotPasswordLink' in data and 'loginDiv' in data and '<div id="stock_simulator">' not in data

    def test_empty_db(self):
        rv = self.test_app.get('/')

        #make sure we are on the login page
        assert self.is_login_page(rv.data)
        assert rv.status_code == 200

    def test_login_fail(self):
        rv = self.login('random_test_email_that_does_not_exist@email.com', 'badPassword')
        assert 'Email and password do not match up' in rv.data
        assert rv.status_code == 200

    def test_create_account_success(self):
        rv = self.create_account("test_account@gmail.com", "test_user_name", "password", "password")

        assert '<div id="stock_simulator">' in rv.data
        assert rv.status_code == 200

    def test_create_account_fail(self):
        rv = self.create_account("test_account@gmail.com", "test_user_name", "password", "not_the_same_password")

        assert self.is_login_page(rv.data)
        assert rv.status_code == 200

if __name__ == '__main__':
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.init_logger()
    app.init_cache('./static/cache.json')
    app.init_db()
    unittest.main()