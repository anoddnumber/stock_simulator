import unittest
from base_unit_test import BaseUnitTest
import simulator
from stock_simulator_test_client import StockSimulatorTestClient


class TestSellStock(BaseUnitTest):

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
                              float(starting_cash) - int(quantity) * float(price))

        rv = self.client.sell_stock(symbol, 1, price)

        self.assert_user_info({symbol: {price.replace(".", "_"): quantity - 1,
                                "total": quantity - 1}},
                      float(starting_cash) - (int(quantity) - 1) * float(price))

        rv = self.client.sell_stock(symbol, 1, price)

        self.assert_user_info({}, starting_cash)
        assert "Success" in rv.data

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

        assert "Stock price or quantity less than 0" in rv.data
        self.assert_user_info({}, starting_cash)

        # does not own any of that stock
        rv = self.client.sell_stock(symbol, 1, price)

        assert "User does not own stock" in rv.data
        self.assert_user_info({}, starting_cash)

        # buy 1 stock and try to sell 2
        quantity_bought = 1
        self.client.buy_stock(symbol, quantity_bought, price)

        self.assert_user_info({symbol: {price.replace(".", "_"): quantity_bought,
                                        "total": quantity_bought}},
                              starting_cash - quantity_bought * float(price))

        rv = self.client.sell_stock(symbol, 2, price)

        print "rv.data: " + str(rv.data)
        assert "User does not own enough stock" in rv.data
        # make sure nothing changed in the db
        self.assert_user_info({symbol: {price.replace(".", "_"): quantity_bought,
                                        "total": quantity_bought}},
                              starting_cash - quantity_bought * float(price))

    def test_sell_bad_symbol(self):
        print "test_sell_bad_symbol"
        self.client.create_account()
        self.client.confirm_test_account()
        self.client.login()

        symbol = "bad_symbol"

        rv = self.client.sell_stock(symbol, 1, 1)
        assert "Invalid symbol" in rv.data

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
                              starting_cash - quantity * float(price))

        # price does not equal server's price
        rv = self.client.sell_stock(symbol, 1, bad_price)

        assert "Stock price changed, please try again." in rv.data
        self.assert_user_info({symbol: {price.replace(".", "_"): quantity,
                               "total": quantity}},
                              starting_cash - quantity * float(price))

        # pass in negative price
        rv = self.client.sell_stock(symbol, 1, -1)

        assert "Stock price or quantity less than 0" in rv.data
        self.assert_user_info({symbol: {price.replace(".", "_"): quantity,
                               "total": quantity}},
                              starting_cash - quantity * float(price))

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
                              starting_cash - quantity * float(price))

        # missing price
        rv = self.client.sell_stock(symbol, quantity, "")

        assert "Error reading arguments" in rv.data
        self.assert_user_info({symbol: {price.replace(".", "_"): quantity,
                                        "total": quantity}},
                              starting_cash - quantity * float(price))

        # missing quantity
        rv = self.client.sell_stock(symbol, "", price)

        assert "Error reading arguments" in rv.data
        self.assert_user_info({symbol: {price.replace(".", "_"): quantity,
                                        "total": quantity}},
                              starting_cash - quantity * float(price))

        # missing symbol
        rv = self.client.sell_stock("", quantity, price)

        print "rv.data: " + rv.data
        assert "Invalid symbol" in rv.data
        self.assert_user_info({symbol: {price.replace(".", "_"): quantity,
                                        "total": quantity}},
                              starting_cash - quantity * float(price))

if __name__ == '__main__':
    unittest.main()