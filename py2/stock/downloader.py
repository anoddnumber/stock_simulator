from py2.clients.alpha_advantage_client import AlphaAdvantageClient

def get_stock_symbols():
    stock_symbols_file = open('data/stock_symbols/11-17-17.txt', 'r')
    stock_symbols = []

    for line in stock_symbols_file:
        symbol_end_index = line.index('|')
        stock_symbol = line[:symbol_end_index]

        if stock_symbol >= "ERIC":
            stock_symbols.append(stock_symbol)

    return stock_symbols

if __name__ == "__main__":
    stock_symbols = get_stock_symbols()
    alpha_advantage_client = AlphaAdvantageClient()

    for symbol in stock_symbols:
        print("writing file for symbol " + str(symbol))
        historical_data = alpha_advantage_client.get_historical_data(symbol)

        history_file = open('./data/' + str(symbol) + '.json', 'w')
        history_file.write(historical_data)
        history_file.close()

