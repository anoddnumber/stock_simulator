from yahoo_api_option import YahooAPIOption, YahooAPIOptions
from yahoo_stock_api_wrapper import YahooStockAPIWrapper
from data_options import DataOptions


class DataRetriever:

    options = [

    ]

    option_to_api_mapping = {
        DataOptions.ASK: YahooAPIOptions.ASK,
        DataOptions.BID: YahooAPIOptions.BID,
        DataOptions.ASK_REAL_TIME: YahooAPIOption('b2'),
        DataOptions.BID_REAL_TIME: YahooAPIOption('b3'),
        DataOptions.PREVIOUS_CLOSE: YahooAPIOption('p'),
        DataOptions.OPEN: YahooAPIOption('o'),
        DataOptions.DIVIDEND_PER_SHARE: YahooAPIOption(''),
        DataOptions.DIVIDEND_PAY_DATE: YahooAPIOption(''),
        DataOptions.EX_DIVIDEND_DATE: YahooAPIOption(''),
        DataOptions.CHANGE: YahooAPIOption(''),
        DataOptions.CHANGE_AND_PERCENT_CHANGE: YahooAPIOption(''),
        DataOptions.CHANGE_REAL_TIME: YahooAPIOption(''),
        DataOptions.CHANGE_PERCENT_REAL_TIME: YahooAPIOption(''),
        DataOptions.CHANGE_IN_PERCENT: YahooAPIOption(''),
        DataOptions.LAST_TRADE_DATE: YahooAPIOption(''),
        DataOptions.TRADE_DATE: YahooAPIOption(''),
        DataOptions.LAST_TRADE_TIME: YahooAPIOption(''),
        DataOptions.AFTER_HOURS_CHANGE_REAL_TIME: YahooAPIOption(''),
        DataOptions.COMMISSION: YahooAPIOption(''),
        DataOptions.DAY_LOW: YahooAPIOption(''),
        DataOptions.DAY_HIGH: YahooAPIOption(''),
        DataOptions.LAST_TRADE_WITH_TIME_REAL_TIME: YahooAPIOption(''),
        DataOptions.LAST_TRADE_WITH_TIME: YahooAPIOption(''),
        DataOptions.LAST_TRADE_PRICE: YahooAPIOptions.LAST_TRADE_PRICE,
        DataOptions.ONE_YEAR_TARGET_PRICE: YahooAPIOption(''),
        DataOptions.CHANGE_FROM_200_DAY_MOVING_AVERAGE: YahooAPIOption(''),
        DataOptions.PERCENT_CHANGE_FROM_200_DAY_MOVING_AVERAGE: YahooAPIOption(''),
        DataOptions.CHANGE_FROM_50_DAY_MOVING_AVERAGE: YahooAPIOption(''),
        DataOptions.PERCENT_CHANGE_FROM_50_DAY_MOVING_AVERAGE: YahooAPIOption(''),
        DataOptions.FIFTY_DAY_MOVING_AVERAGE: YahooAPIOption(''),
        DataOptions.TWO_HUNDRED_DAY_MOVING_AVERAGE: YahooAPIOption(''),
        DataOptions.DAY_VALUE_CHANGE: YahooAPIOption(''),
        DataOptions.DAY_VALUE_CHANGE_REAL_TIME: YahooAPIOption(''),
        DataOptions.PRICE_PAID: YahooAPIOption(''),
        DataOptions.DAY_RANGE: YahooAPIOption(''),
        DataOptions.DAY_RANGE_REAL_TIME: YahooAPIOption(''),
        DataOptions.HOLDINGS_GAIN_PERCENT: YahooAPIOption(''),
        DataOptions.ANNUALIZED_GAIN: YahooAPIOption(''),
        DataOptions.HOLDINGS_GAIN: YahooAPIOption(''),
        DataOptions.HOLDINGS_GAIN_PERCENT_REAL_TIME: YahooAPIOption(''),
        DataOptions.HOLDINGS_GAIN_REAL_TIME: YahooAPIOption(''),
        DataOptions.FIFTY_TWO_WEEK_HIGH: YahooAPIOption(''),
        DataOptions.FIFTY_TWO_WEEK_LOW: YahooAPIOption(''),
        DataOptions.CHANGE_FROM_FIFTY_TWO_WEEK_LOW: YahooAPIOption(''),
        DataOptions.CHANGE_FROM_FIFTY_TWO_WEEK_HIGH: YahooAPIOption(''),
        DataOptions.PERCENT_CHANGE_FROM_FIFTY_TWO_WEEK_LOW: YahooAPIOption(''),
        DataOptions.PERCENT_CHANGE_FROM_FIFTY_TWO_WEEK_HIGH: YahooAPIOption(''),
        DataOptions.FIFTY_TWO_WEEK_RANGE: YahooAPIOption(''),
        DataOptions.MORE_INFO: YahooAPIOption(''),
        DataOptions.MARKET_CAPITALIZATION: YahooAPIOption(''),
        DataOptions.MARKET_CAP_REAL_TIME: YahooAPIOption(''),
        DataOptions.FLOAT_SHARES: YahooAPIOption(''),
        DataOptions.NAME: YahooAPIOption(''),
        DataOptions.NOTES: YahooAPIOption(''),
        DataOptions.SYMBOL: YahooAPIOption(''),
        DataOptions.SHARES_OWNED: YahooAPIOption(''),
        DataOptions.STOCK_EXCHANGE: YahooAPIOption(''),
        DataOptions.SHARES_OUTSTANDING: YahooAPIOption(''),
        DataOptions.VOLUME: YahooAPIOption(''),
        DataOptions.ASK_SIZE: YahooAPIOption(''),
        DataOptions.BID_SIZE: YahooAPIOption(''),
        DataOptions.LAST_TRADE_SIZE: YahooAPIOption(''),
        DataOptions.AVERAGE_DAILY_VOLUME: YahooAPIOption(''),
        DataOptions.TICKER_TREND: YahooAPIOption(''),
        DataOptions.TRADE_LINKS: YahooAPIOption(''),
        DataOptions.ORDER_BOOK_REAL_TIME: YahooAPIOption(''),
        DataOptions.HIGH_LIMIT: YahooAPIOption(''),
        DataOptions.LOW_LIMIT: YahooAPIOption(''),
        DataOptions.HOLDINGS_VALUE: YahooAPIOption(''),
        DataOptions.HOLDINGS_VALUE_REAL_TIME: YahooAPIOption(''),
        DataOptions.REVENUE: YahooAPIOption(''),
        DataOptions.EARNINGS_PER_SHARE: YahooAPIOption(''),
        DataOptions.EPS_ESTIMATE_CURRENT_YEAR: YahooAPIOption(''),
        DataOptions.EPS_ESTIMATE_NEXT_YEAR: YahooAPIOption(''),
        DataOptions.EPS_ESTIMATE_NEXT_QUARTER: YahooAPIOption(''),
        DataOptions.BOOK_VALUE: YahooAPIOption(''),
        DataOptions.EBITDA: YahooAPIOption(''),
        DataOptions.PRICE_SALES: YahooAPIOption(''),
        DataOptions.PRICE_BOOK: YahooAPIOption(''),
        DataOptions.P_E_RATIO: YahooAPIOption(''),
        DataOptions.P_E_RATIO_REAL_TIME: YahooAPIOption(''),
        DataOptions.PEG_RATIO: YahooAPIOption(''),
        DataOptions.PRICE_EPS_ESTIMATE_CURRENT_YEAR: YahooAPIOption(''),
        DataOptions.PRICE_EPS_ESTIMATE_NEXT_YEAR: YahooAPIOption(''),
        DataOptions.SHORT_RATIO: YahooAPIOption('')
    }

    @staticmethod
    def get_data(stocks, options):
        yahoo_options = []
        for option in options:
            api_option = DataRetriever.option_to_api_mapping.get(option)
            if isinstance(api_option, YahooAPIOption):
                yahoo_options.append(api_option.get_option())

        return YahooStockAPIWrapper.get_data2(stocks, yahoo_options)
