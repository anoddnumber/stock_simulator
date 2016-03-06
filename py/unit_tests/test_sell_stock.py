import unittest
from base_unit_test import BaseUnitTest
import simulator

class TestSellStock(BaseUnitTest):

    def test_basic_sell(self):
        print "test_basic_sell"
        self.client.create_account()

        symbol = "AMZN"
        quantity = 1
        price = self.client.get_stock_info(symbol).data
        starting_cash = simulator.config.get("defaultCash")

        self.client.buy_stock(symbol, quantity, price)

        self.assert_user_info({symbol : {price.replace(".", "_") : quantity} },
                              starting_cash - quantity * float(price))

        rv = self.client.sell_stock(symbol, quantity, price)

        self.assert_user_info({}, starting_cash)
        assert "Success" in rv.data

    def test_sell_without_account(self):
        print "test_sell_without_account"

        symbol = "AMZN"
        price = self.client.get_stock_info(symbol).data

        rv = self.client.sell_stock(symbol, 1, price)
        assert "Not logged in, cannot sell stock." in rv.data

    def test_sell_bad_quantity(self):
        print "test_sell_bad_quantity"
        self.client.create_account()

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

        self.assert_user_info({symbol : {price.replace(".", "_") : quantity_bought} },
                      starting_cash - quantity_bought * float(price))

        rv = self.client.sell_stock(symbol, 2, price)

        assert "User down not enough stock" in rv.data
        # make sure nothing changed in the db
        self.assert_user_info({symbol : {price.replace(".", "_") : quantity_bought} },
              starting_cash - quantity_bought * float(price))

if __name__ == '__main__':
    unittest.main()