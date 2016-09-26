import unittest
from base_unit_test import BaseUnitTest
import simulator
from stock_simulator_test_client import StockSimulatorTestClient
from py.constants import errors
from py.constants.errors import ERROR_CODE_MAP


class TestSellStock(BaseUnitTest):

    @staticmethod
    def assert_sell_successful(data):
        assert "You have successfully sold" in data

    @staticmethod
    def assert_cannot_read_args(data):
        TestSellStock.assert_error_symbol(errors.UNEXP, data)

    @staticmethod
    def assert_negative_price(data):
        TestSellStock.assert_error_symbol(errors.UNEXP, data)

    @staticmethod
    def assert_sell_too_few(data):
        TestSellStock.assert_error_symbol(errors.SLESS, data)

    @staticmethod
    def assert_not_enough_stock_owned(data):
        TestSellStock.assert_error_symbol(errors.NESTK, data)

    @staticmethod
    def assert_stock_does_not_exist(data):
        TestSellStock.assert_error_symbol(errors.SDNE, data)

    @staticmethod
    def assert_stock_price_changed(data):
        TestSellStock.assert_error_symbol(errors.PRICH, data)

    @staticmethod
    def assert_error_symbol(err_sym, data):
        assert ERROR_CODE_MAP.get(err_sym) in data

    def test_basic_sell(self):
        print "test_basic_sell"
        self.client.create_account()
        self.client.confirm_test_account()
        self.client.login()

        symbol = "AMZN"
        quantity = 2
        price = self.client.get_stock_info(symbol).data
        starting_cash = simulator.config.get("defaultCash")

        self.client.buy_stock(symbol, quantity, price)

        self.assert_user_info({symbol: {price.replace(".", "_"): quantity,
                                        "total": quantity}},
                              float(starting_cash) - int(quantity) * float(price) - simulator.config['commission'])

        rv = self.client.sell_stock(symbol, 1, price)

        self.assert_user_info({symbol: {price.replace(".", "_"): quantity - 1,
                               "total": quantity - 1}},
                              float(starting_cash) - (int(quantity) - 1) * float(price) - simulator.config['commission'])

        TestSellStock.assert_sell_successful(rv.data)

        rv = self.client.sell_stock(symbol, 1, price)

        TestSellStock.assert_sell_successful(rv.data)
        self.assert_user_info({}, starting_cash - simulator.config['commission'])

    def test_sell_without_account(self):
        print "test_sell_without_account"

        symbol = "AMZN"
        # price = self.client.get_stock_info(symbol).data
        price = 123
        rv = self.client.sell_stock(symbol, 1, price)
        assert StockSimulatorTestClient.is_login_page(rv.data)

    def test_sell_bad_quantity(self):
        print "test_sell_bad_quantity"
        self.client.create_account()
        self.client.confirm_test_account()
        self.client.login()

        symbol = "AMZN"
        starting_cash = simulator.config.get("defaultCash")
        price = self.client.get_stock_info(symbol).data

        self.assert_user_info({}, starting_cash)

        # negative quantity
        rv = self.client.sell_stock(symbol, -1, price)

        TestSellStock.assert_sell_too_few(rv.data)
        self.assert_user_info({}, starting_cash)

        # does not own any of that stock
        rv = self.client.sell_stock(symbol, 1, price)

        TestSellStock.assert_not_enough_stock_owned(rv.data)
        self.assert_user_info({}, starting_cash)

        # buy 1 stock and try to sell 2
        quantity_bought = 1
        self.client.buy_stock(symbol, quantity_bought, price)

        self.assert_user_info({symbol: {price.replace(".", "_"): quantity_bought,
                                        "total": quantity_bought}},
                              starting_cash - quantity_bought * float(price) - simulator.config['commission'])

        rv = self.client.sell_stock(symbol, 2, price)

        TestSellStock.assert_not_enough_stock_owned(rv.data)
        # make sure nothing changed in the db
        self.assert_user_info({symbol: {price.replace(".", "_"): quantity_bought,
                                        "total": quantity_bought}},
                              starting_cash - quantity_bought * float(price) - simulator.config['commission'])

    def test_sell_bad_symbol(self):
        print "test_sell_bad_symbol"
        self.client.create_account()
        self.client.confirm_test_account()
        self.client.login()

        symbol = "bad_symbol"

        rv = self.client.sell_stock(symbol, 1, 1)
        TestSellStock.assert_stock_does_not_exist(rv.data)

    def test_sell_bad_stock_price(self):
        print "test_sell_bad_stock_price"
        self.client.create_account()
        self.client.confirm_test_account()
        self.client.login()

        symbol = "AMZN"
        quantity = 1
        starting_cash = simulator.config.get("defaultCash")
        price = self.client.get_stock_info(symbol).data
        bad_price = float(price) - 1

        self.assert_user_info({}, starting_cash)

        self.client.buy_stock(symbol, quantity, price)

        self.assert_user_info({symbol : {price.replace(".", "_"): quantity,
                                         "total": quantity}},
                              starting_cash - quantity * float(price) - simulator.config['commission'])

        # price does not equal server's price
        rv = self.client.sell_stock(symbol, 1, bad_price)

        TestSellStock.assert_stock_price_changed(rv.data)
        self.assert_user_info({symbol: {price.replace(".", "_"): quantity,
                               "total": quantity}},
                              starting_cash - quantity * float(price) - simulator.config['commission'])

        # pass in negative price
        rv = self.client.sell_stock(symbol, 1, -1)

        TestSellStock.assert_negative_price(rv.data)
        self.assert_user_info({symbol: {price.replace(".", "_"): quantity,
                               "total": quantity}},
                              starting_cash - quantity * float(price) - simulator.config['commission'])

    def test_sell_missing_argument(self):
        print "test_sell_missing_argument"
        self.client.create_account()
        self.client.confirm_test_account()
        self.client.login()

        symbol = "AMZN"
        quantity = 1
        starting_cash = simulator.config.get("defaultCash")
        price = self.client.get_stock_info(symbol).data

        self.assert_user_info({}, starting_cash)

        self.client.buy_stock(symbol, quantity, price)

        self.assert_user_info({symbol: {price.replace(".", "_"): quantity,
                                        "total": quantity}},
                              starting_cash - quantity * float(price) - simulator.config['commission'])

        # missing price
        rv = self.client.sell_stock(symbol, quantity, "")

        TestSellStock.assert_cannot_read_args(rv.data)
        self.assert_user_info({symbol: {price.replace(".", "_"): quantity,
                                        "total": quantity}},
                              starting_cash - quantity * float(price) - simulator.config['commission'])

        # missing quantity
        rv = self.client.sell_stock(symbol, "", price)

        TestSellStock.assert_cannot_read_args(rv.data)
        self.assert_user_info({symbol: {price.replace(".", "_"): quantity,
                                        "total": quantity}},
                              starting_cash - quantity * float(price) - simulator.config['commission'])

        # missing symbol
        rv = self.client.sell_stock("", quantity, price)

        TestSellStock.assert_cannot_read_args(rv.data)
        self.assert_user_info({symbol: {price.replace(".", "_"): quantity,
                                        "total": quantity}},
                              starting_cash - quantity * float(price) - simulator.config['commission'])

if __name__ == '__main__':
    unittest.main()