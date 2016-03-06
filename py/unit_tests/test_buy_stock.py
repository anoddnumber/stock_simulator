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
        quantity = int(starting_cash / float(price) + 1)
        rv = self.client.buy_stock(symbol, quantity, price)

        assert "Not enough cash" in rv.data

        self.assert_user_info({}, starting_cash)


if __name__ == '__main__':
    unittest.main()