import os
import json
from yahoo_stock_api import YahooStockAPI
import datetime

class Cache:
    
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
            
    def getLastUpdatedDate(self):
        if self.parsed_json is None:
            return None
        last_updated_date = datetime.datetime.strptime(self.parsed_json['last_updated'], "%Y-%m-%d %H:%M:%S.%f")
        return last_updated_date
    
    def update(self, timeInMinutes = 0):
        last_updated_date = self.getLastUpdatedDate()
        if last_updated_date is not None:
            limit = datetime.timedelta(minutes = timeInMinutes)
            difference = datetime.datetime.now() - self.getLastUpdatedDate()
            if difference > limit:
                self.updateCache()
        else:
            print 'no last_updated_date found'
            self.updateCache()
            
            
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
    
    def addResultsToNewCache(self, newJson, keys, results):
        for i, key in enumerate(keys):
            newJson[key] = results[i]
            
    def getStockPrices(self, symbols):
        prices = ''
        for symbol in symbols:
            try:
                prices += self.parsed_json[symbol] + '\n'
            except KeyError, e:
                print "Stock symbol " + symbol + " not found"
        return prices
        