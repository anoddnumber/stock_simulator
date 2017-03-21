from yahoo_api_option import YahooAPIOption, YahooAPIOptions
from yahoo_stock_api_wrapper import YahooStockAPIWrapper
from data_options import DataOptions


class DataRetriever:

    option_to_api_mapping = {
        DataOptions.ASK: YahooAPIOptions.ASK,
        DataOptions.BID: YahooAPIOptions.BID,
        DataOptions.ASK_REAL_TIME: YahooAPIOptions.ASK_REAL_TIME,
        DataOptions.BID_REAL_TIME: YahooAPIOptions.BID_REAL_TIME,
        DataOptions.PREVIOUS_CLOSE: YahooAPIOptions.PREVIOUS_CLOSE,
        DataOptions.OPEN: YahooAPIOptions.OPEN,
        DataOptions.DIVIDEND_PER_SHARE: YahooAPIOptions.DIVIDEND_PER_SHARE,
        DataOptions.DIVIDEND_PAY_DATE: YahooAPIOptions.DIVIDEND_PAY_DATE,
        DataOptions.EX_DIVIDEND_DATE: YahooAPIOptions.EX_DIVIDEND_DATE,
        DataOptions.CHANGE: YahooAPIOptions.CHANGE,
        DataOptions.CHANGE_AND_PERCENT_CHANGE: YahooAPIOptions.CHANGE_AND_PERCENT_CHANGE,
        DataOptions.CHANGE_REAL_TIME: YahooAPIOptions.CHANGE_REAL_TIME,
        DataOptions.CHANGE_PERCENT_REAL_TIME: YahooAPIOptions.CHANGE_PERCENT_REAL_TIME,
        DataOptions.CHANGE_IN_PERCENT: YahooAPIOptions.CHANGE_IN_PERCENT,
        DataOptions.LAST_TRADE_DATE: YahooAPIOptions.LAST_TRADE_DATE,
        DataOptions.TRADE_DATE: YahooAPIOptions.TRADE_DATE,
        DataOptions.LAST_TRADE_TIME: YahooAPIOptions.LAST_TRADE_TIME,
        DataOptions.AFTER_HOURS_CHANGE_REAL_TIME: YahooAPIOptions.AFTER_HOURS_CHANGE_REAL_TIME,
        DataOptions.COMMISSION: YahooAPIOptions.COMMISSION,
        DataOptions.DAY_LOW: YahooAPIOptions.DAY_LOW,
        DataOptions.DAY_HIGH: YahooAPIOptions.DAY_HIGH,
        DataOptions.LAST_TRADE_WITH_TIME_REAL_TIME: YahooAPIOptions.LAST_TRADE_WITH_TIME_REAL_TIME,
        DataOptions.LAST_TRADE_WITH_TIME: YahooAPIOptions.LAST_TRADE_WITH_TIME,
        DataOptions.LAST_TRADE_PRICE: YahooAPIOptions.LAST_TRADE_PRICE,
        DataOptions.ONE_YEAR_TARGET_PRICE: YahooAPIOptions.ONE_YEAR_TARGET_PRICE,
        DataOptions.CHANGE_FROM_200_DAY_MOVING_AVERAGE: YahooAPIOptions.CHANGE_FROM_200_DAY_MOVING_AVERAGE,
        DataOptions.PERCENT_CHANGE_FROM_200_DAY_MOVING_AVERAGE: YahooAPIOptions.PERCENT_CHANGE_FROM_200_DAY_MOVING_AVERAGE,
        DataOptions.CHANGE_FROM_50_DAY_MOVING_AVERAGE: YahooAPIOptions.CHANGE_FROM_50_DAY_MOVING_AVERAGE,
        DataOptions.PERCENT_CHANGE_FROM_50_DAY_MOVING_AVERAGE: YahooAPIOptions.PERCENT_CHANGE_FROM_50_DAY_MOVING_AVERAGE,
        DataOptions.FIFTY_DAY_MOVING_AVERAGE: YahooAPIOptions.FIFTY_DAY_MOVING_AVERAGE,
        DataOptions.TWO_HUNDRED_DAY_MOVING_AVERAGE: YahooAPIOptions.TWO_HUNDRED_DAY_MOVING_AVERAGE,
        DataOptions.DAY_VALUE_CHANGE: YahooAPIOptions.DAY_VALUE_CHANGE,
        DataOptions.DAY_VALUE_CHANGE_REAL_TIME: YahooAPIOptions.DAY_VALUE_CHANGE_REAL_TIME,
        DataOptions.PRICE_PAID: YahooAPIOptions.PRICE_PAID,
        DataOptions.DAY_RANGE: YahooAPIOptions.DAY_RANGE,
        DataOptions.DAY_RANGE_REAL_TIME: YahooAPIOptions.DAY_RANGE_REAL_TIME,
        DataOptions.HOLDINGS_GAIN_PERCENT: YahooAPIOptions.HOLDINGS_GAIN_PERCENT,
        DataOptions.ANNUALIZED_GAIN: YahooAPIOptions.ANNUALIZED_GAIN,
        DataOptions.HOLDINGS_GAIN: YahooAPIOptions.HOLDINGS_GAIN,
        DataOptions.HOLDINGS_GAIN_PERCENT_REAL_TIME: YahooAPIOptions.HOLDINGS_GAIN_PERCENT_REAL_TIME,
        DataOptions.HOLDINGS_GAIN_REAL_TIME: YahooAPIOptions.HOLDINGS_GAIN_REAL_TIME,
        DataOptions.FIFTY_TWO_WEEK_HIGH: YahooAPIOptions.FIFTY_TWO_WEEK_HIGH,
        DataOptions.FIFTY_TWO_WEEK_LOW: YahooAPIOptions.FIFTY_TWO_WEEK_LOW,
        DataOptions.CHANGE_FROM_FIFTY_TWO_WEEK_LOW: YahooAPIOptions.CHANGE_FROM_FIFTY_TWO_WEEK_LOW,
        DataOptions.CHANGE_FROM_FIFTY_TWO_WEEK_HIGH: YahooAPIOptions.CHANGE_FROM_FIFTY_TWO_WEEK_HIGH,
        DataOptions.PERCENT_CHANGE_FROM_FIFTY_TWO_WEEK_LOW: YahooAPIOptions.PERCENT_CHANGE_FROM_FIFTY_TWO_WEEK_LOW,
        DataOptions.PERCENT_CHANGE_FROM_FIFTY_TWO_WEEK_HIGH: YahooAPIOptions.PERCENT_CHANGE_FROM_FIFTY_TWO_WEEK_HIGH,
        DataOptions.FIFTY_TWO_WEEK_RANGE: YahooAPIOptions.FIFTY_TWO_WEEK_RANGE,
        DataOptions.MORE_INFO: YahooAPIOptions.MORE_INFO,
        DataOptions.MARKET_CAPITALIZATION: YahooAPIOptions.MARKET_CAPITALIZATION,
        DataOptions.MARKET_CAP_REAL_TIME: YahooAPIOptions.MARKET_CAP_REAL_TIME,
        DataOptions.FLOAT_SHARES: YahooAPIOptions.FLOAT_SHARES,
        DataOptions.NAME: YahooAPIOptions.NAME,
        DataOptions.NOTES: YahooAPIOptions.NOTES,
        DataOptions.SYMBOL: YahooAPIOptions.SYMBOL,
        DataOptions.SHARES_OWNED: YahooAPIOptions.SHARES_OWNED,
        DataOptions.STOCK_EXCHANGE: YahooAPIOptions.STOCK_EXCHANGE,
        DataOptions.SHARES_OUTSTANDING: YahooAPIOptions.SHARES_OUTSTANDING,
        DataOptions.VOLUME: YahooAPIOptions.VOLUME,
        DataOptions.ASK_SIZE: YahooAPIOptions.ASK_SIZE,
        DataOptions.BID_SIZE: YahooAPIOptions.BID_SIZE,
        DataOptions.LAST_TRADE_SIZE: YahooAPIOptions.LAST_TRADE_SIZE,
        DataOptions.AVERAGE_DAILY_VOLUME: YahooAPIOptions.AVERAGE_DAILY_VOLUME,
        DataOptions.TICKER_TREND: YahooAPIOptions.TICKER_TREND,
        DataOptions.TRADE_LINKS: YahooAPIOptions.TRADE_LINKS,
        DataOptions.ORDER_BOOK_REAL_TIME: YahooAPIOptions.ORDER_BOOK_REAL_TIME,
        DataOptions.HIGH_LIMIT: YahooAPIOptions.HIGH_LIMIT,
        DataOptions.LOW_LIMIT: YahooAPIOptions.LOW_LIMIT,
        DataOptions.HOLDINGS_VALUE: YahooAPIOptions.HOLDINGS_VALUE,
        DataOptions.HOLDINGS_VALUE_REAL_TIME: YahooAPIOptions.HOLDINGS_VALUE_REAL_TIME,
        DataOptions.REVENUE: YahooAPIOptions.REVENUE,
        DataOptions.EARNINGS_PER_SHARE: YahooAPIOptions.EARNINGS_PER_SHARE,
        DataOptions.EPS_ESTIMATE_CURRENT_YEAR: YahooAPIOptions.EPS_ESTIMATE_CURRENT_YEAR,
        DataOptions.EPS_ESTIMATE_NEXT_YEAR: YahooAPIOptions.EPS_ESTIMATE_NEXT_YEAR,
        DataOptions.EPS_ESTIMATE_NEXT_QUARTER: YahooAPIOptions.EPS_ESTIMATE_NEXT_QUARTER,
        DataOptions.BOOK_VALUE: YahooAPIOptions.BOOK_VALUE,
        DataOptions.EBITDA: YahooAPIOptions.EBITDA,
        DataOptions.PRICE_SALES: YahooAPIOptions.PRICE_SALES,
        DataOptions.PRICE_BOOK: YahooAPIOptions.PRICE_BOOK,
        DataOptions.P_E_RATIO: YahooAPIOptions.P_E_RATIO,
        DataOptions.P_E_RATIO_REAL_TIME: YahooAPIOptions.P_E_RATIO_REAL_TIME,
        DataOptions.PEG_RATIO: YahooAPIOptions.PEG_RATIO,
        DataOptions.PRICE_EPS_ESTIMATE_CURRENT_YEAR: YahooAPIOptions.PRICE_EPS_ESTIMATE_CURRENT_YEAR,
        DataOptions.PRICE_EPS_ESTIMATE_NEXT_YEAR: YahooAPIOptions.PRICE_EPS_ESTIMATE_NEXT_YEAR,
        DataOptions.SHORT_RATIO: YahooAPIOptions.SHORT_RATIO
    }

    @staticmethod
    def get_data(stocks, options):
        yahoo_options = []
        for option in options:
            api_option = DataRetriever.option_to_api_mapping.get(option)
            if isinstance(api_option, YahooAPIOption):
                yahoo_options.append(api_option.get_option())

        return YahooStockAPIWrapper.get_data2(stocks, yahoo_options)
