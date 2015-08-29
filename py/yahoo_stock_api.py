from urllib2 import Request, urlopen, URLError

class YahooStockAPI:
    '''
        stock_symbols - The symbol of the stock that you want information for
        info_arguments - What type of information you want. The arguments you can specify are documented here:
        http://www.jarloo.com/yahoo_finance/
    '''
    def __init__(self, stock_symbols, info_arguments):
        self.ss = stock_symbols;
        self.info = info_arguments;
        
    def submitRequest(self):
        if len(self.ss) > 200:
            return 'Too many stock symbols requested. Please request at most 200 stock symbols. Exiting.'
        symbols = ""
        for s in self.ss:
            symbols += s + '+'
        request = Request('http://finance.yahoo.com/d/quotes.csv?s=' + symbols + '&f=' + self.info)
        
        try:
            response = urlopen(request)
            text = response.read()
            print text
            return text
        except URLError, e:
            print 'Error in sending/receiving request/reply: ', e
            return 'There was an error retreiving stock information. Please try again.'