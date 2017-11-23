from urllib2 import Request, urlopen, URLError


class AlphaAdvantageClient:
    api_key = 'S86TTOVAFIWT3D8B'

    def get_historical_data(self, symbol):
        request = Request('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&'
                          'symbol=' + str(symbol) +
                          '&outputsize=full&apikey=S86TTOVAFIWT3D8B')

        try:
            print "before url open, request: " + str(request.get_full_url())
            response = urlopen(request)
            print "response received"
            text = response.read()
            print "returning text"
            return text
        except URLError, error:
            print "URL Error! : " + str(error)
            # self.logger.exception("Error in sending/receiving request/reply: ")


# alpha_advantage_client = AlphaAdvantageClient()
# print alpha_advantage_client.get_historical_data('AMZN')
