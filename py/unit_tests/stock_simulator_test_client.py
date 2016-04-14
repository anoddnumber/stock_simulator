import simulator
from test_info import TestInfo


class StockSimulatorTestClient:

    def __init__(self):
        # simulator.config['TESTING'] = True
        simulator.config['DEBUG'] = True  # Set to bypass reCaptcha
        simulator.app.config['TESTING'] = True  # Set so that no emails are send during testing
        simulator.init_logger()
        simulator.init_cache('./static/cache.json')
        simulator.init_db()

        self.client = simulator.app.test_client()

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Your __exit__() method's return value determines what happens next if the block raised an exception.
        If it returns True, Python ignores the exception and proceeds with execution at a point just after the with block.
        If you don't want your context manager to suppress the exception, don't re-raise it explicitly, just return False
        and Python will then re-raise the exception.
        """
        self.client.__exit__(exc_type, exc_val, exc_tb)
        return False

    def login(self, email=TestInfo.email, password=TestInfo.password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password,
        ), follow_redirects=True)

    def create_account(self, email=TestInfo.email, username=TestInfo.user_name, password=TestInfo.password, retype_password=TestInfo.password):
        return self.client.post('/createAccount', data=dict(
            email=email,
            username=username,
            password=password,
            retypePassword=retype_password,
        ), follow_redirects=True)

    def logout(self):
        return self.client.post('/logout', data=dict(), follow_redirects=True)

    def buy_stock(self, symbol, quantity, stock_price):
        return self.client.post('/buyStock', data=dict(
            symbol=symbol,
            quantity=quantity,
            stockPrice=stock_price,
        ), follow_redirects=True)

    def sell_stock(self, symbol, quantity, stock_price):
        return self.client.post('/sellStock', data=dict(
            symbol=symbol,
            quantity=quantity,
            stockPrice=stock_price,
        ), follow_redirects=True)

    def get_stock_info(self, symbols):
        return self.client.get('/info?symbols=' + str(symbols))

    def get(self, path, follow_redirects=True):
        return self.client.get(path, follow_redirects=follow_redirects)

    @staticmethod
    def is_login_page(data):
        return 'forgotPasswordLink' in data and 'loginDiv' in data and '<div id="stock_simulator">' not in data

    @staticmethod
    def is_simulator_page(data):
        return '<div id="stock_simulator">' in data

    # only useful if follow_redirects is false
    @staticmethod
    def is_redirect(data, redirect_route=None):
        result = 'You should be redirected automatically to target URL:' in data
        if redirect_route is not None:
            result = result and redirect_route in data
        return result

    @staticmethod
    def is_cookie_set(response_headers):
        return 'Set-Cookie' in str(response_headers)