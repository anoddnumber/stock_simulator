import app

class TestClient:
    test_user_name = "test_user_name"
    test_email = "test_email@gmail.com"
    test_password = "password"

    def __init__(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.init_logger()
        app.init_cache('./static/cache.json')
        app.init_db()
        self.client = app.application.test_client()

    def login(self, email=test_email, password=test_password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password,
        ), follow_redirects=True)

    def create_account(self, email=test_email, username=test_user_name, password=test_password, retype_password=test_password):
        return self.client.post('/createAccount', data=dict(
            email=email,
            username=username,
            password=password,
            retypePassword=retype_password,
        ), follow_redirects=True)

    def logout(self):
        return self.client.post('/logout', data=dict(), follow_redirects=True)

    def get(self, path, follow_redirects=True):
        return self.client.get(path, follow_redirects=follow_redirects)

    @staticmethod
    def is_login_page(data):
        return 'forgotPasswordLink' in data and 'loginDiv' in data and '<div id="stock_simulator">' not in data

    @staticmethod
    def is_simulator_page(data):
        return '<div id="stock_simulator">' in data

    @staticmethod
    def is_redirect(data, redirect_route=None):
        result = 'You should be redirected automatically to target URL:' in data
        if redirect_route is not None:
            result = result and redirect_route in data
        return result