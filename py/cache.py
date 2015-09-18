import os
import json
import datetime
from invalid_usage import InvalidUsage
from yahoo_stock_api import YahooStockAPI
from decimal import Decimal

"""
The cache is responsible for having fast access to stock price information.
It also allows clients to update it to make sure the information is not stale.
The cache updates by calling the YahooStockApi and completely replaces the cache with the new information.
"""
class Cache:
    """
    Creates the cache. If the path does not exist, create it by updating the cache.
    """
    def __init__(self):
        #current directory is always /stock_simulator
        self.path = './static/cache.json' 
        self.parsed_json = None #the object that holds the cache info
        
        try:
            cache = open(self.path, 'r')
            json_string = ''
            for line in cache:
                json_string += line
            self.parsed_json = json.loads(json_string)
            self.update()
        except (ValueError, IOError) as e:
            print e
            self.update()
            
    """
    Returns the last datetime that the cache was updated.
    Looks in the cache for the last_updated key and returns the value.
    A sample datetime would be 2015-09-07 19:07:51.870404
    """
    def getLastUpdatedDate(self):
        if self.parsed_json is None:
            return None
        last_updated_date = datetime.datetime.strptime(self.parsed_json['last_updated'], "%Y-%m-%d %H:%M:%S.%f")
        return last_updated_date
    
    """
    Updates the cache if timeInMinutes minutes have passed since the last time it was updated
    or if there is no last updated date found (Either the cache does not exist or is corrupted).
    
    timeInMinutes - the number of minutes that should have passed before actually updating the cache
    """
    def update(self, timeInMinutes = 0):
        last_updated_date = self.getLastUpdatedDate()
        if last_updated_date is not None:
            limit = datetime.timedelta(minutes = timeInMinutes)
            difference = datetime.datetime.now() - last_updated_date
            if difference > limit:
                self.__updateCache()
        else:
            print 'no last_updated_date found'
            self.__updateCache()
            
    """
    Finds what symbols should be updated. Updates the parsed_json field, which holds the cache data as a variable.
    Updates the cache.json file.
    """
    def __updateCache(self):
        #current directory is always /stock_simulator
        parsed_symbols_file = open('./static/parsed_symbols.json', 'r')
        json_string = ''
        for line in parsed_symbols_file:
            json_string += line
            
        self.parsed_json = self.__getNewJson(json.loads(json_string))
#         self.loadCacheFromFile() #for testing purposes only
        
        cacheFile = open(self.path, 'w')
        json.dump(self.parsed_json, cacheFile, indent=1, sort_keys='true')
    
    """
    Builds up the new cache and returns it
    
    symbolNameJson - the json object (a dictionary) that contains the symbol to name mapping
    """
    def __getNewJson(self, symbolNameJson):
        keys = sorted(symbolNameJson.keys())
        newJson = json.loads("{}")
        keysToSend = []
        names = []
        maxKeysToSend = 200 # Yahoo's API takes at most 200 symbols at a time
        
        for i, key in enumerate(keys):
            if i is not 0 and i % maxKeysToSend == 0:
                self.__addResultsToNewCache(newJson, keysToSend, names)
                keysToSend = []
                names = []
            keysToSend.append(key)
            names.append(symbolNameJson[key])
        self.__addResultsToNewCache(newJson, keysToSend, names)
        newJson['last_updated'] = str(datetime.datetime.now())
        
        return newJson
    
    """
    Helps to build the new cache
    Calls Yahoo's Stock API to get up to date stock prices. Builds a JSON object with the stock symbols as keys and
    the price as the value. This JSON object represents the new cache.
    
    newJson - the JSON object to populate.
    keys - an array of keys (strings) to be inserted into the JSON object.
    names - an array of names (strings) of the stocks that we are retreiving that will be inserted into the JSON object
    """
    def __addResultsToNewCache(self, newJson, keys, names):
        api = YahooStockAPI(keys, 'l1')
        results = api.submitRequest()
        results = [x.strip() for x in results.split('\n', len(keys) - 1)]
        
        if len(keys) != len(results):
            raise InvalidUsage('Server Cache Error, keys and results do not match', status_code=500)
        for i, key in enumerate(keys):
            try:
                name = names[i]
                decimal = Decimal(float(results[i]))
                price = str('{:.2f}'.format(round(decimal, 2)))
                newJson[key] = {"name": str(name), "price" : price}
            except ValueError as e:
                continue
    
    """
    Returns stock prices (as strings) that are delimited by newlines ("\n").
    
    symbols - an array of symbols whose stock prices will be returned
    """
    def getStockPrices(self, symbols):
        prices = ''
        for i, symbol in enumerate(symbols):
            try:
                info = self.parsed_json[symbol]
                price = info["price"]
                if i == len(symbols) - 1:
                    prices += price
                else:
                    prices += price + '\n'
            except KeyError, e:
                print e
                print "Stock symbol " + symbol + " not found"
        return prices
    
    def loadCacheFromFile(self):
        cacheFile = open('./static/cache.json', 'r')
        json_string = ''
        for line in cacheFile:
            json_string += line
        
        newJson = json.loads(json_string)
        newJson['last_updated'] = str(datetime.datetime.now())
        self.parsed_json = newJson
        
        