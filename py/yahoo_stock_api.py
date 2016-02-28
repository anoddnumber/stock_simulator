from urllib2 import Request, urlopen, URLError
from py.exceptions.invalid_usage import InvalidUsage
import logging

class YahooStockAPI:
    """
        stock_symbols - The symbol of the stock that you want information for
        info_arguments - What type of information you want. The arguments you can specify are documented here:
        http://www.jarloo.com/yahoo_finance/
    """
    def __init__(self, stock_symbols, info_arguments):
        self.ss = stock_symbols
        self.info = info_arguments
        self.logger = logging.getLogger(__name__)
        
    def submit_request(self):
        if len(self.ss) > 200:
            raise InvalidUsage('Too many stock symbols requested. Please request at most 200 stock symbols. Exiting.', status_code=501)
        symbols = ""
        for s in self.ss:
            symbols += s + '+'

        self.logger.info("Calling Yahoo's Finance API with " + str(self.info) + " as the parameters " +
                         " for symbols " + str(symbols))
        request = Request('http://finance.yahoo.com/d/quotes.csv?s=' + str(symbols) + '&f=' + str(self.info))

        try:
            response = urlopen(request)
            text = response.read()
            return text
        except URLError:
            self.logger.exception("Error in sending/receiving request/reply: ")
            raise InvalidUsage('There was an error retrieving stock information. Please try again.', status_code=503)