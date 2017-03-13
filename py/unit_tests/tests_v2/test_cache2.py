import unittest
from cache2 import Cache2
from utility import merge_two_dicts, merge_n_dicts

class Cache2Test(unittest.TestCase):

    CNSL = "CNSL"
    CNTF = "CNTF"
    NON_EXISTENT_SYMBOL = "non_existent_symbol"

    CNSL_MAP = {CNSL: {
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

    CNSL2_MAP = {CNSL: {
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

    CNTF_MAP = {CNTF: {
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

    NON_EXISTENT_SYMBOL_MAP = {NON_EXISTENT_SYMBOL: None}

    def setUp(self):
        self.cache = Cache2()
        assert self.cache.get_all() == {}

    def tearDown(self):
        pass

    def test_get(self):
        data = self.cache.get([Cache2Test.NON_EXISTENT_SYMBOL])
        assert data == {Cache2Test.NON_EXISTENT_SYMBOL: None}

        self.cache.store(Cache2Test.CNSL_MAP)
        data = self.cache.get([Cache2Test.CNSL])
        assert data == Cache2Test.CNSL_MAP
        data = self.cache.get([Cache2Test.CNSL, Cache2Test.NON_EXISTENT_SYMBOL])
        assert data == merge_two_dicts(Cache2Test.CNSL_MAP, Cache2Test.NON_EXISTENT_SYMBOL_MAP)

        self.cache.store(Cache2Test.CNTF_MAP)
        data = self.cache.get([Cache2Test.CNSL])
        assert data == Cache2Test.CNSL_MAP
        data = self.cache.get([Cache2Test.CNSL, Cache2Test.CNTF])
        assert data == merge_two_dicts(Cache2Test.CNSL_MAP, Cache2Test.CNTF_MAP)
        data = self.cache.get([Cache2Test.CNSL, Cache2Test.CNTF, Cache2Test.NON_EXISTENT_SYMBOL])
        assert data == merge_n_dicts([Cache2Test.CNSL_MAP, Cache2Test.CNTF_MAP, Cache2Test.NON_EXISTENT_SYMBOL_MAP])

    def test_get_all(self):
        self.cache.store(Cache2Test.CNSL_MAP)
        data = self.cache.get_all()
        assert data == Cache2Test.CNSL_MAP

        self.cache.store(Cache2Test.CNTF_MAP)
        data = self.cache.get_all()
        assert data == merge_two_dicts(Cache2Test.CNSL_MAP, Cache2Test.CNTF_MAP)

    def test_get_symbols(self):
        data = self.cache.get_symbols()
        assert data == []

        self.cache.store(Cache2Test.CNSL_MAP)
        data = self.cache.get_symbols()
        assert data == [Cache2Test.CNSL]

        self.cache.store(Cache2Test.CNTF_MAP)
        data = self.cache.get_symbols()
        assert data == [Cache2Test.CNTF, Cache2Test.CNSL]

    def test_store(self):
        self.cache.store(Cache2Test.CNSL_MAP)
        assert self.cache.get_all() == Cache2Test.CNSL_MAP

        #replace the previous CNSL value
        self.cache.store(Cache2Test.CNSL2_MAP)
        assert self.cache.get_all() == Cache2Test.CNSL2_MAP

        self.cache.store(Cache2Test.CNTF_MAP)
        merged_dict = merge_two_dicts(Cache2Test.CNSL2_MAP, Cache2Test.CNTF_MAP)
        assert self.cache.get_all() == merged_dict

    def test_remove(self):
        self.cache.remove(Cache2Test.NON_EXISTENT_SYMBOL) # This should not cause any exceptions

        self.cache.store(Cache2Test.CNSL_MAP)
        self.cache.remove(Cache2Test.CNSL)
        data = self.cache.get_all()
        assert data == {}

        self.cache.store(Cache2Test.CNSL_MAP)
        self.cache.store(Cache2Test.CNTF_MAP)
        self.cache.remove(Cache2Test.NON_EXISTENT_SYMBOL)
        data = self.cache.get_all()
        assert data == merge_two_dicts(Cache2Test.CNSL_MAP, Cache2Test.CNTF_MAP)

        self.cache.remove(Cache2Test.CNSL)
        data = self.cache.get_all()
        assert data == Cache2Test.CNTF_MAP

        self.cache.store(Cache2Test.CNSL_MAP)
        data = self.cache.get_all()
        assert data == merge_two_dicts(Cache2Test.CNSL_MAP, Cache2Test.CNTF_MAP)
        self.cache.remove([Cache2Test.CNSL, Cache2Test.CNTF])
        data = self.cache.get_all()
        assert data == {}

    def test_clear(self):
        self.cache.clear()
        data = self.cache.get_all()
        assert data == {}

        self.cache.store(Cache2Test.CNSL_MAP)
        self.cache.clear()
        data = self.cache.get_all()
        assert data == {}

        self.cache.store(Cache2Test.CNSL_MAP)
        self.cache.store(Cache2Test.CNTF_MAP)
        self.cache.clear()
        data = self.cache.get_all()
        assert data == {}

    def test_replace(self):
        self.cache.store(Cache2Test.CNSL_MAP)
        self.cache.replace(Cache2Test.CNTF_MAP)
        data = self.cache.get_all()
        assert data == Cache2Test.CNTF_MAP

        self.cache.store(Cache2Test.CNSL_MAP)
        self.cache.replace({})
        data = self.cache.get_all()
        assert data == {}

if __name__ == '__main__':
    unittest.main()