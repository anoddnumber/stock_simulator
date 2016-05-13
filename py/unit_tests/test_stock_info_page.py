import unittest
from base_unit_test import BaseUnitTest
# from stock_simulator_test_client import StockSimulatorTestClient


class TestStockInfo(BaseUnitTest):

    def test_basic_stock_info(self):
        print "test_basic_stock_info"

        self.client.create_account()

        self.client.confirm_test_account()
        self.client.login()

        self.client.stock_info_page("AMZN")


if __name__ == '__main__':
    unittest.main()