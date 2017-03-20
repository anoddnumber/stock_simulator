from yahoo_stock_api import YahooStockAPI
from utility import merge_two_dicts


class YahooStockAPIWrapper:

    arguments_map = {
        # Pricing
        'a': 'Ask',
        'b': 'Bid',
        'b2': 'Ask (Realtime)',
        'b3': 'Bid (Realtime)',
        'p': 'Previous Close',
        'o': 'Open',

        # Dividends
        'y': 'Dividend Yield',
        'd': 'Dividend per Share',
        'r1': 'Dividend Pay Date',
        'q': 'Ex-Dividend Date',

        # Date
        'c1': 'Change',
        'c': 'Change & Percent Change',
        'c6': 'Change (Realtime)',
        'k2': 'Change Percent (Realtime)',
        'p2': 'Change in Percent',
        'd1': 'Last Trade Date',
        'd2': 'Trade Date',
        't1': 'Last Trade Time',

        # Averages
        'c8': 'After Hours Change (Realtime)',
        'c3': 'Commission',
        'g': 'Day\'s Low',
        'h': 'Day\'s High',
        'k1': 'Last Trade (Realtime) With Time',
        'l': 'Last Trade (With Time)',
        'l1': 'Last Trade (Price Only)',
        't8': '1 yr Target Price',
        'm5': 'Change From 200 Day Moving Average',
        'm6': 'Percent Change From 200 Day Moving Average',
        'm7': 'Change From 50 Day Moving Average',
        'm8': 'Percent Change From 50 Day Moving Average',
        'm3': '50 Day Moving Average',
        'm4': '200 Day Moving Average',

        # Misc
        'w1': 'Day\'s Value Change',
        'w4': 'Day\'s Value Change (Realtime)',
        'p1': 'Price Paid',
        'm': 'Day\'s Range',
        'm2': 'Day\'s Range (Realtime)',
        'g1': 'Holdings Gain Percent',
        'g3': 'Annualized Gain',
        'g4': 'Holdings Gain',
        'g5': 'Holdings Gain Percent (Realtime)',
        'g6': 'Holdings Gain (Realtime)',

        # 52 week pricing
        'k': '52 Week High',
        'j': '52 week Low',
        'j5': 'Change From 52 Week Low',
        'k4': 'Change From 52 week High',
        'j6': 'Percent Change From 52 week Low',
        'k5': 'Percent Change From 52 week High',
        'w': '52 week Range',

        # Symbol info
        'i': 'More Info',
        'j1': 'Market Capitalization',
        'j3': 'Market Cap (Realtime)',
        'f6': 'Float Shares',
        'n': 'Name',
        'n4': 'Notes',
        's': 'Symbol',
        's1': 'Shares Owned',
        'x': 'Stock Exchange',
        'j2': 'Shares Outstanding',

        # Volume
        'v': 'Volume',
        'a5': 'Ask Size',
        'b6': 'Bid Size',
        'k3': 'Last Trade Size',
        'a2': 'Average Daily Volume',

        # Misc
        't7': 'Ticker Trend',
        't6': 'Trade Links',
        'i5': 'Order Book (Realtime)',
        'l2': 'High Limit',
        'l3': 'Low Limit',
        'v1': 'Holdings Value',
        'v7': 'Holdings Value (Realtime)',
        's6': 'Revenue',

        # Ratios
        'e': 'Earnings per Share',
        'e7': 'EPS Estimate Current Year',
        'e8': 'EPS Estimate Next Year',
        'e9': 'EPS Estimate Next Quarter',
        'b4': 'Book Value',
        'j4': 'EBITDA',
        'p5': 'Price / Sales',
        'p6': 'Price / Book',
        'r': 'P/E Ratio',
        'r2': 'P/E Ratio (Realtime)',
        'r5': 'PEG Ratio',
        'r6': 'Price / EPS Estimate Current Year',
        'r7': 'Price / EPS Estimate Next Year',
        's7': 'Short Ratio',
    }

    @staticmethod
    def get_data(stocks, options):
        start = 0
        end = YahooStockAPI.MAX_STOCKS_PER_CALL
        yahoo_api_options = ''.join(options)
        result = {}

        while start < len(stocks):
            api = YahooStockAPI(stocks[start:end], yahoo_api_options)
            api_result = api.submit_request()
            api_result = YahooStockAPIWrapper._format_api_result(stocks[start:end], options, api_result)

            result = merge_two_dicts(result, api_result)

            start += YahooStockAPI.MAX_STOCKS_PER_CALL
            end += YahooStockAPI.MAX_STOCKS_PER_CALL

        return result

    @staticmethod
    def get_data2(stocks, options):
        """
        Retrieves stock data
        :param stocks: list of stock symbols
        :param options: list of YahooAPIOption objects
        :return: map of stock data
        """
        yahoo_options = []
        for option in options:
            yahoo_options.append(option.get_yahoo_option())
        yahoo_api_args = ''.join(yahoo_options)

        start = 0
        end = YahooStockAPI.MAX_STOCKS_PER_CALL
        result = {}
        while start < len(stocks):
            api = YahooStockAPI(stocks[start:end], yahoo_api_args)
            api_result = api.submit_request()
            api_result = YahooStockAPIWrapper._format_api_result2(stocks[start:end], options, api_result)

            result = merge_two_dicts(result, api_result)

            start += YahooStockAPI.MAX_STOCKS_PER_CALL
            end += YahooStockAPI.MAX_STOCKS_PER_CALL

        return result

    @staticmethod
    def _format_api_result(stocks, options, results):
        # rstrip removes trailing newline characters
        results = results.rstrip().split('\n')
        rtn = {}

        for stock, result in zip(stocks, results):
            data = result.split(',')
            rtn[stock] = YahooStockAPIWrapper._format_stock(options, data)

        return rtn

    @staticmethod
    def _format_api_result2(stocks, options, results):
        # rstrip removes trailing newline characters
        results = results.rstrip().split('\n')
        rtn = {}

        for stock, result in zip(stocks, results):
            data = result.split(',')
            rtn[stock] = YahooStockAPIWrapper._format_stock2(options, data)

        return rtn

    @staticmethod
    def _format_stock(options, data):
        stock_info = {}
        for option, datum in zip(options, data):
            option_value = YahooStockAPIWrapper.arguments_map.get(option)
            if option_value is None:
                continue
            stock_info[option_value] = datum
        return stock_info

    @staticmethod
    def _format_stock2(options, data):
        stock_info = {}
        for option, datum in zip(options, data):
            stock_info[option.get_option()] = datum
        return stock_info

if __name__ == '__main__':
    from yahoo_api_option import YahooAPIOptions
    # formatted = YahooStockAPIWrapper.get_data(['MSFT', 'AMZN', 'AAL', 'ARNA', 'AROW', 'ARQL'], ['l1', 'c1'])
    # print "formatted: " + str(formatted)
    formatted = YahooStockAPIWrapper.get_data2(['MSFT', 'AMZN', 'AAL', 'ARNA', 'AROW', 'ARQL'], [YahooAPIOptions.LAST_TRADE_PRICE, YahooAPIOptions.ASK])
    print "formatted: " + str(formatted)
