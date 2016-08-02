import unittest
from base_unit_test import BaseUnitTest
import simulator
from stock_simulator_test_client import StockSimulatorTestClient
from py.constants import errors
from py.constants.errors import ERROR_CODE_MAP


# TODO: Test buying a stock at different prices (somewhat difficult to test this..)
class TestBuyStock(BaseUnitTest):

    @staticmethod
    def assert_buy_successful(data):
        assert "You have successfully bought" in data

    @staticmethod
    def assert_cannot_read_args(data):
        TestBuyStock.assert_error_symbol(errors.UNEXP, data)

    @staticmethod
    def assert_negative_price(data):
        TestBuyStock.assert_error_symbol(errors.UNEXP, data)

    @staticmethod
    def assert_buy_too_few(data):
        TestBuyStock.assert_error_symbol(errors.BLESS, data)

    @staticmethod
    def assert_not_enough_cash(data):
        TestBuyStock.assert_error_symbol(errors.BNEC, data)

    @staticmethod
    def assert_stock_does_not_exist(data):
        TestBuyStock.assert_error_symbol(errors.SDNE, data)

    @staticmethod
    def assert_stock_price_changed(data):
        TestBuyStock.assert_error_symbol(errors.PRICH, data)

    @staticmethod
    def assert_error_symbol(err_sym, data):
        assert ERROR_CODE_MAP.get(err_sym) in data

    def test_basic_buy(self):
        print "test_basic_buy"
        self.client.create_account()
        self.client.confirm_test_account()
        self.client.login()

        symbol = "AMZN"
        starting_cash = simulator.config.get("defaultCash")
        quantity = 1
        price = self.client.get_stock_info(symbol).data

        self.assert_user_info({}, starting_cash)

        rv = self.client.buy_stock(symbol, quantity, price)

        TestBuyStock.assert_buy_successful(rv.data)
        self.assert_user_info({symbol: {price.replace(".", "_"): quantity, "total": quantity}},
                              starting_cash - quantity * float(price) - simulator.config['commission'])

        # buy the same stock again
        rv = self.client.buy_stock(symbol, quantity, price)

        TestBuyStock.assert_buy_successful(rv.data)
        self.assert_user_info({symbol: {price.replace(".", "_"): quantity * 2, "total": quantity * 2}},
                              starting_cash - quantity * float(price) * 2 - simulator.config['commission'] * 2)

    def test_buy_as_much_as_possible(self):
        print "test_buy_as_much_as_possible"
        self.client.create_account()
        self.client.confirm_test_account()
        self.client.login()

        symbol = "AMZN"
        starting_cash = simulator.config.get("defaultCash")

        rv = self.client.get_stock_info(symbol)
        price = rv.data

        self.assert_user_info({}, starting_cash)

        max_quantity_possible = int( (starting_cash - simulator.config['commission']) / float(price))
        rv = self.client.buy_stock(symbol, max_quantity_possible, price)

        TestBuyStock.assert_buy_successful(rv.data)
        self.assert_user_info({symbol: {price.replace(".", "_"): max_quantity_possible,
                                        "total": max_quantity_possible
                                        }},
                              starting_cash - max_quantity_possible * float(price) - simulator.config['commission'])

    def test_buy_without_account(self):
        print "test_buy_without_account"
        symbol = "AMZN"

        rv = self.client.get_stock_info(symbol)
        price = rv.data

        rv = self.client.buy_stock(symbol, 1, price)
        assert StockSimulatorTestClient.is_login_page(rv.data)

    def test_buy_bad_quantity(self):
        print "test_buy_bad_quantity"
        self.client.create_account()
        self.client.confirm_test_account()
        self.client.login()

        symbol = "AMZN"
        starting_cash = simulator.config.get("defaultCash")
        price = self.client.get_stock_info(symbol).data

        self.assert_user_info({}, starting_cash)

        # negative quantity
        rv = self.client.buy_stock(symbol, -1, price)

        TestBuyStock.assert_buy_too_few(rv.data)
        self.assert_user_info({}, starting_cash)

        # too much quantity
        too_much_quantity = int(float(starting_cash) / float(price) + 1)
        rv = self.client.buy_stock(symbol, too_much_quantity, price)

        TestBuyStock.assert_not_enough_cash(rv.data)
        self.assert_user_info({}, starting_cash)

    def test_buy_bad_symbol(self):
        print "test_buy_bad_symbol"
        self.client.create_account()
        self.client.confirm_test_account()
        self.client.login()

        symbol = "bad_symbol"

        rv = self.client.buy_stock(symbol, 1, 1)
        TestBuyStock.assert_stock_does_not_exist(rv.data)

    def test_buy_bad_stock_price(self):
        print "test_buy_bad_stock_price"
        self.client.create_account()
        self.client.confirm_test_account()
        self.client.login()

        symbol = "AMZN"
        quantity = 1
        starting_cash = simulator.config.get("defaultCash")
        price = self.client.get_stock_info(symbol).data
        bad_price = float(price) - 1

        self.assert_user_info({}, starting_cash)

        # price does not equal server's price
        rv = self.client.buy_stock(symbol, quantity, bad_price)

        TestBuyStock.assert_stock_price_changed(rv.data)
        self.assert_user_info({}, starting_cash)

        # pass in negative price
        rv = self.client.buy_stock(symbol, quantity, -1)

        TestBuyStock.assert_negative_price(rv.data)
        self.assert_user_info({}, starting_cash)

    def test_buy_missing_argument(self):
        print "test_buy_missing_argument"
        self.client.create_account()
        self.client.confirm_test_account()
        self.client.login()

        symbol = "AMZN"
        quantity = 1
        starting_cash = simulator.config.get("defaultCash")
        price = self.client.get_stock_info(symbol).data

        self.assert_user_info({}, starting_cash)

        # missing price
        rv = self.client.buy_stock(symbol, quantity, "")

        TestBuyStock.assert_cannot_read_args(rv.data)
        self.assert_user_info({}, starting_cash)

        # missing quantity
        rv = self.client.buy_stock(symbol, "", price)

        TestBuyStock.assert_cannot_read_args(rv.data)
        self.assert_user_info({}, starting_cash)

        # missing symbol
        rv = self.client.buy_stock("", quantity, price)

        TestBuyStock.assert_cannot_read_args(rv.data)
        self.assert_user_info({}, starting_cash)

if __name__ == '__main__':
    unittest.main()