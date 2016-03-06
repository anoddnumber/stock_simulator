import unittest
import ast
from base_unit_test import BaseUnitTest
import simulator

#TODO: Test buying a stock at different prices (somewhat difficult to test this..)
class TestBuyStock(BaseUnitTest):

    def test_basic_buy(self):
        print "test_basic_buy"
        self.client.create_account()

        symbol = "AMZN"

        rv = self.client.get_stock_info(symbol)
        price = rv.data

        rv = self.client.get('/getUserInfo')
        user_dict = ast.literal_eval(rv.data)

        assert user_dict.get('stocks_owned') == {}
        starting_cash = float(user_dict.get('cash'))

        self.client.buy_stock(symbol, 1, price)

        rv = self.client.get('/getUserInfo')
        user_dict = ast.literal_eval(rv.data)

        assert user_dict.get('stocks_owned') != {}
        assert float(user_dict.get('cash')) == starting_cash - float(price)

        price = price.replace(".", "_")
        assert user_dict.get('stocks_owned').get(symbol).get(price) == 1

    def test_buy_as_much_as_possible(self):
        print "test_buy_as_much_as_possible"
        self.client.create_account()

        symbol = "AMZN"

        rv = self.client.get_stock_info(symbol)
        price = rv.data

        user_dict = self.assert_user_info({}, simulator.config.get("defaultCash"))
        starting_cash = float(user_dict.get('cash'))

        self.assert_user_info({}, starting_cash)

        max_quantity_possible = int(starting_cash / float(price))
        rv = self.client.buy_stock(symbol, max_quantity_possible, price)

        assert "Success" in rv.data

        self.assert_user_info({"AMZN" : {price.replace(".", "_") : max_quantity_possible} },
                              starting_cash - max_quantity_possible * float(price))

    def test_buy_without_account(self):
        print "test_buy_without_account"
        symbol = "AMZN"

        rv = self.client.get_stock_info(symbol)
        price = rv.data

        rv = self.client.buy_stock(symbol, 1, price)
        assert "Not logged in, cannot buy stock." in rv.data

    def test_bad_quantity(self):
        print "test_bad_quantity"
        self.client.create_account()

        symbol = "AMZN"

        rv = self.client.get_stock_info(symbol)
        price = rv.data

        user_dict = self.assert_user_info({}, simulator.config.get("defaultCash"))
        starting_cash = float(user_dict.get('cash'))

        # negative quantity
        rv = self.client.buy_stock(symbol, -1, price)
        assert "Stock price or quantity less than 0" in rv.data

        self.assert_user_info({}, starting_cash)

        # too much quantity
        too_much_quantity = int(starting_cash / float(price) + 1)
        rv = self.client.buy_stock(symbol, too_much_quantity, price)

        assert "Not enough cash" in rv.data

        self.assert_user_info({}, starting_cash)

    def test_bad_symbol(self):
        print "test_bad_symbol"
        self.client.create_account()

        symbol = "bad_symbol"

        # negative quantity
        rv = self.client.buy_stock(symbol, 1, 1)
        assert "Invalid symbol" in rv.data

    def test_bad_stock_price(self):
        print "test_bad_stock_price"
        self.client.create_account()

        symbol = "AMZN"

        rv = self.client.get_stock_info(symbol)
        price = rv.data
        bad_price = float(price) - 1

        user_dict = self.assert_user_info({}, simulator.config.get("defaultCash"))
        starting_cash = float(user_dict.get('cash'))

        # price does not equal server's price
        rv = self.client.buy_stock(symbol, 1, bad_price)
        assert "Stock price changed, please try again." in rv.data

        self.assert_user_info({}, starting_cash)

        # pass in negative price
        rv = self.client.buy_stock(symbol, 1, -1)

        assert "Stock price or quantity less than 0" in rv.data

        self.assert_user_info({}, starting_cash)

if __name__ == '__main__':
    unittest.main()