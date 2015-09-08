import os
import json
from yahoo_stock_api import YahooStockAPI
import datetime

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
        self.parsed_json = None
        
        try:
            cache = open(self.path, 'r')
            json_string = ''
            for line in cache:
                json_string += line
            self.parsed_json = json.loads(json_string)
        except IOError, e:
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
                self.updateCache()
        else:
            print 'no last_updated_date found'
            self.updateCache()
            
    """
    Actually updates the cache by calling YahooStockAPI.
    YahooStockAPI can only take 200 symbols at a time. Thus, break the requests to contain 200 or fewer symbols at a time.
    Save the results in a new JSON object, append a last_updated key with the current time as the value, 
    sort it alphabetically by keys, and store it in the cache at the end.
    
    TODO: make private, and refactor.
    """
    def updateCache(self):
        #current directory is always /stock_simulator
        parsed_symbols_file = open('./static/parsed_symbols.json', 'r')
        json_string = ''
        for line in parsed_symbols_file:
            json_string += line
            
        keys = json.loads(json_string).keys()
        keys.sort()
        newJson = json.loads("{}")
        keysToSend = []
        
        for i, key in enumerate(keys):
            if i is not 0 and i % 200 == 0:
                api = YahooStockAPI(keysToSend, 'l1')
                results = api.submitRequest()
                self.addResultsToNewCache(newJson, keysToSend, [x.strip() for x in results.split('\n')])
                keysToSend = []
            keysToSend.append(key)
            
        self.addResultsToNewCache(newJson, keysToSend, [x.strip() for x in results.split('\n')])
        newJson['last_updated'] = str(datetime.datetime.now())
        self.parsed_json = newJson
        
        cache = open(self.path, 'w')
        json.dump(newJson, cache, indent=1, sort_keys='true')
    
    """
    Builds the new JSON object with the given keys/results.
    This JSON object represents the new cache.
    
    newJson - the JSON object to populate.
    keys - an array of keys (strings) to be inserted into the JSON object.
    results - an array of results (strings) corresponding to the given keys.
    
    TODO: make private
    """
    def addResultsToNewCache(self, newJson, keys, results):
        for i, key in enumerate(keys):
            newJson[key] = results[i]
    
    """
    Returns stock prices that are delimited by newlines ("\n").
    
    symbols - an array of symbols whose stock prices will be returned
    """
    def getStockPrices(self, symbols):
        prices = ''
        for symbol in symbols:
            try:
                prices += self.parsed_json[symbol] + '\n'
            except KeyError, e:
                print "Stock symbol " + symbol + " not found"
        return prices
        