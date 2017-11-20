from py2.clients.alpha_advantage_client import AlphaAdvantageClient

def get_stock_symbols():
    cache = open(path, 'r')
    json_string = ''
    for line in cache:
        json_string += line

if __name__ == "__main__":
    alpha_advantage_client = AlphaAdvantageClient()
    historical_data = alpha_advantage_client.get_historical_data("MSFT")

    history_file = open('./data/MSFT.json', 'w')
    history_file.write(historical_data)
    history_file.close()

