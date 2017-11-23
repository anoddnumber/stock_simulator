import json


class AlphaAdvantageDataLoader:

    def __init__(self):
        pass

    def get_data(self, date, symbols):
        snapshot = {}
        for symbol in symbols:
            with open('../../stock/data/' + str(symbol) + '.json', 'r') as history_file:
                # for line in history_file:
                #     print(line)
                try:
                    my_json = json.load(history_file)
                    snapshot[symbol] = my_json['Time Series (Daily)'][date]
                except Exception:
                    print "Failed to get data for symbol " + str(symbol) + " and date " + str(date)
                    continue
                # print my_json['Time Series (Daily)']['2015-11-19']
        return snapshot


if __name__ == "__main__":
    loader = AlphaAdvantageDataLoader()
    print loader.get_data('2015-11-19', ['AMZN', 'CHRW', 'CHEF'])
