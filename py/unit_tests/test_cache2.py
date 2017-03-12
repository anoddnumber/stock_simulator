import unittest
from cache2 import Cache2
from utility import merge_two_dicts

class Cache2Test(unittest.TestCase):

    CNSL = {"CNSL": {
      "daily_percent_change": "+2.45%",
      "daily_price_change": "+0.55",
      "day_high": "23.66",
      "day_low": "22.78",
      "day_open": "23.45",
      "div_yield": "6.89",
      "market_cap": "1.17B",
      "name": "Consolidated Communications Holdings, Inc.",
      "pe_ratio": "80.52",
      "price": "23.03"
    }}

    CNSL2 = {"CNSL": {
      "daily_percent_change": "+3.45%",
      "daily_price_change": "+3.55",
      "day_high": "3.66",
      "day_low": "2.78",
      "day_open": "3.45",
      "div_yield": ".89",
      "market_cap": "2.17B",
      "name": "Consolidated Communications Holdings, Inc.",
      "pe_ratio": "8.52",
      "price": "25.32"
    }}

    CNTF = {"CNTF": {
      "daily_percent_change": "+31.06%",
      "daily_price_change": "+0.50",
      "day_high": "2.11",
      "day_low": "1.57",
      "day_open": "1.72",
      "div_yield": "N/A",
      "market_cap": "22.34M",
      "name": "China TechFaith Wireless Communication Technology Limited",
      "pe_ratio": "N/A",
      "price": "2.11"
    }}

    def setUp(self):
        print "setup"
        self.cache = Cache2()
        assert self.cache.get_all() == {}

    def tearDown(self):
        pass


    def test_store(self):
        self.cache.store(Cache2Test.CNSL)
        assert self.cache.get_all() == Cache2Test.CNSL

        #replace the previous CNSL value
        self.cache.store(Cache2Test.CNSL2)
        assert self.cache.get_all() == Cache2Test.CNSL2

        self.cache.store(Cache2Test.CNTF)
        merged_dict = merge_two_dicts(Cache2Test.CNSL2, Cache2Test.CNTF)
        assert self.cache.get_all() == merged_dict


if __name__ == '__main__':
    unittest.main()