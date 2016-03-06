import unittest
import ast
from base_unit_test import BaseUnitTest

#TODO: Test buying a stock at different prices (somewhat difficult to test this..)
class TestBuyStock(BaseUnitTest):

    def test_basic_buy(self):
        print "\ntest_basic_buy"
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

if __name__ == '__main__':
    unittest.main()