import os
import app
import unittest
import tempfile

class TestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.test_app = app.application.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def login(self, email, password):
        return self.test_app.post('/login', data=dict(
            email=email,
            password=password,
        ), follow_redirects=True)

    def test_empty_db(self):
        rv = self.test_app.get('/')

        #make sure we are on the login page
        assert 'forgotPasswordLink' in rv.data and 'loginDiv' in rv.data

    def test_login(self):
        rv = self.login('random_test_email_that_does_not_exist@email.com', 'badPassword')
        assert 'Email and password do not match up' in rv.data

if __name__ == '__main__':
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.init_logger()
    app.init_cache('./static/cache.json')
    app.init_db()
    unittest.main()