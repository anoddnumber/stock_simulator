
class Cache2:

    def __init__(self):
        self.map = {}

    def get(self, symbols_map):
        return {k: self.map[k] for k in symbols_map.keys()}

    def get_all(self):
        return self.map

    def get_symbols(self):
        return self.map.keys()

    def store(self, symbols_map):
        symbols = symbols_map.keys()
        for symbol in symbols:
            self.map[symbol] = symbols_map[symbol]

    def remove(self, symbols):
        for symbol in symbols:
            del self.map[symbol]

    def clear(self):
        self.map = {}

    def replace(self, new_map):
        self.map = new_map