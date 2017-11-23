from urllib2 import Request, urlopen, URLError


class AlphaAdvantageClient:
    api_key = 'S86TTOVAFIWT3D8B'

    def get_historical_data(self, symbol):
        request = Request('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&'
                          'symbol=' + symbol +
                          '&outputsize=full&apikey=S86TTOVAFIWT3D8B')

        try:
            response = urlopen(request)
            text = response.read()
            return text
        except URLError:
            print "URL Error!"
            # self.logger.exception("Error in sending/receiving request/reply: ")


# alpha_advantage_client = AlphaAdvantageClient()
# print alpha_advantage_client.get_historical_data('AMZN')
