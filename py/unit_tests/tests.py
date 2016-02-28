import os
import app
import unittest
import tempfile

class TestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.test_app = app.application.test_client()
        app.init_logger()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.test_app.get('/')

        #make sure we are on the login page
        assert 'forgotPasswordLink' in rv.data and 'loginDiv' in rv.data

if __name__ == '__main__':
    unittest.main()