

class StockSymbols:
    """
    Determines what symbols we should query for/have in our cache.
    """

    @staticmethod
    def get_symbols():
        return StockSymbols.get_symbols_from_file()

    @staticmethod
    def get_symbols_from_file():
        # current directory is always /stock_simulator
        parsed_symbols_file = open('./static/parsed_symbols.json', 'r')

        symbols_list = []

        for line in parsed_symbols_file:
            # the symbol should be the characters between the first and second double quotes
            # the first double quotes is always the first character in the line
            end = line.find('"', 2)
            if end > 1:
                symbols_list.append(line[1:end])
        return symbols_list


if __name__ == "__main__":
    print "get_symbols: " + str(StockSymbols.get_symbols())