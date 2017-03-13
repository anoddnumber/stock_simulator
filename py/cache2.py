import json

class Cache2:
    """
    The cache keeps track of stock data. Its purpose is for the application to keep the data itself and not have
    to call an API every time to get the information.
    """

    def __init__(self):
        self.map = {}

    def get(self, symbols):
        return {k: self.map.get(k) for k in symbols}

    def get_all(self):
        return self.map

    def get_symbols(self):
        return self.map.keys()

    def store(self, symbols_map):
        symbols = symbols_map.keys()
        for symbol in symbols:
            self.map[symbol] = symbols_map[symbol]

    def remove(self, symbols):
        if isinstance(symbols, basestring):
            symbols = [symbols]

        for symbol in symbols:
            self.map.pop(symbol, None)

    def clear(self):
        self.map = {}

    def replace(self, new_map):
        self.map = new_map

    def save_to_file(self, path='./static/cache2.json'):
        cache_file = open(path, 'w')
        json.dump(self.map, cache_file, indent=1, sort_keys='true')
