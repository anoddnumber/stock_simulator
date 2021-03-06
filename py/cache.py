import json
import datetime
import time
from decimal import Decimal

from py.exceptions.invalid_usage import InvalidUsage
from yahoo_stock_api import YahooStockAPI
import logging


# TODO: retrieve the NASDAQ file daily (currently called stock_symbols.txt)
# and generate the json file daily (currently called parsed_symbols.json).
class Cache:
    """
    The cache is responsible for having fast access to stock price information.
    It also allows clients to update it to make sure the information is not stale.
    The cache updates by calling the YahooStockApi and completely replaces the cache with the new information.
    """

    def __init__(self, load_from_file_path=None):
        """
        Creates the cache. If the path does not exist, create it by updating the cache.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initialized cache logger")

        # current directory is always /stock_simulator
        self.path = './static/cache.json'
        self.parsed_json = None  # the object that holds the cache info
        self.load_from_file_path = load_from_file_path

        try:
            self.logger.info("Trying to load the cache from file")
            cache = open(self.path, 'r')
            json_string = ''
            for line in cache:
                json_string += line
            self.parsed_json = json.loads(json_string)
            self.logger.info("Successfully loaded cache from file")
        except (ValueError, IOError) as e:
            self.logger.exception("Error while loading cache")

    @property
    def json(self):
        return self.parsed_json

    def get_last_updated_date(self):
        """
        Returns the last datetime that the cache was updated.
        Looks in the cache for the last_updated key and returns the value.
        A sample datetime would be 2015-09-07 19:07:51.870404
        """
        if self.parsed_json is None:
            return None
        last_updated_date = datetime.datetime.strptime(self.parsed_json['last_updated'], "%Y-%m-%dT%H:%M:%S.%f")
        return last_updated_date

    def update(self, time_in_minutes=0):
        """
        Updates the cache if timeInMinutes minutes have passed since the last time it was updated
        or if there is no last updated date found (Either the cache does not exist or is corrupted).

        timeInMinutes - the number of minutes that should have passed before actually updating the cache
        returns the number of seconds until the next expected update
        """
        time_in_seconds = time_in_minutes * 60
        try:
            last_updated_date = self.get_last_updated_date()
        except (KeyError, ValueError):
            self.logger.exception("last_updated_date has bad format - updating cache to fix it")
            self.__update_cache()
            return time_in_seconds

        if last_updated_date is not None:
            limit = datetime.timedelta(minutes=time_in_minutes)
            difference = datetime.datetime.utcnow() - last_updated_date

            if difference > limit:
                self.logger.info("The difference, " + str(difference) + ", is greater than the limit, " + str(limit) +
                                 ", so the cache will update")
                self.__update_cache()
                return time_in_seconds
            else:
                seconds = (limit - difference).total_seconds()
                self.logger.info("Still waiting " + str(seconds) + " seconds until cache will update")
                return seconds
        else:
            self.logger.warning("no last_updated_date found in cache, updating the cache")
            self.__update_cache()
            return time_in_seconds

    def __update_cache(self):
        """
        Finds what symbols should be updated. Updates the parsed_json field, which holds the cache data as a variable.
        Updates the cache.json file.
        """
        self.logger.info("Attempting to update the cache")
        # current directory is always /stock_simulator
        parsed_symbols_file = open('./static/parsed_symbols.json', 'r')
        json_string = ''
        for line in parsed_symbols_file:
            json_string += line

        if self.load_from_file_path is not None:
            self.load_cache_from_file() # for testing purposes only
        else:
            self.parsed_json = self.__get_new_json(json.loads(json_string))
        
        cache_file = open(self.path, 'w')
        json.dump(self.parsed_json, cache_file, indent=1, sort_keys='true')
        self.logger.info("Finished updating the cache")

    def __get_new_json(self, symbol_name_json):
        """
        Builds up the new cache and returns it

        symbol_name_json - the json object (a dictionary) that contains the symbol to name mapping
        """
        keys = sorted(symbol_name_json.keys())
        # self.logger.info("Attempting to update the following keys in the cache: " + str(keys))
        new_json = json.loads("{}")
        keys_to_send = []
        names = []
        max_keys_to_send = 200 # Yahoo's API takes at most 200 symbols at a time
        
        for i, key in enumerate(keys):
            if i is not 0 and i % max_keys_to_send == 0:
                self.__add_results_to_new_cache(new_json, keys_to_send, names)
                keys_to_send = []
                names = []
                time.sleep(1)
            keys_to_send.append(key)
            names.append(symbol_name_json[key])
        self.__add_results_to_new_cache(new_json, keys_to_send, names)
        new_json['last_updated'] = str(datetime.datetime.utcnow().isoformat())
        
        return new_json

    def __add_results_to_new_cache(self, new_json, keys, names):
        """
        Helps to build the new cache
        Calls Yahoo's Stock API to get up to date stock prices. Builds a JSON object with the stock symbols as keys and
        the price as the value. This JSON object represents the new cache.

        newJson - the JSON object to populate.
        keys - an array of keys (strings) to be inserted into the JSON object.
        names - an array of names (strings) of the stocks that we are retrieving that will be inserted into the JSON object
        """
        api = YahooStockAPI(keys, 'l1c1p2ohgj1ry')

        try:
            results = api.submit_request()
            results = [x.strip() for x in results.split('\n', len(keys) - 1)]
            # self.logger.info("results from YahooStockAPI: " + str(results))

            if len(keys) != len(results):
                self.logger.error("Calling YahooStockAPI unsuccessful, the number of keys and results do not match.")
                self.logger.error("len(keys): " + str(len(keys)))
                self.logger.error("len(results: " + str(len(results)))
                raise InvalidUsage('Server Cache Error, keys and results do not match', status_code=500)

            for i, key in enumerate(keys):
                try:
                    name = names[i]
                    line = results[i]
                    (decimal, daily_price_change, daily_percent_change, day_open, day_high, day_low, market_cap,
                     pe_ratio, div_yield) = tuple(line.split(','))

                    try:
                        decimal = Decimal(float(decimal))
                        price = str('{:.2f}'.format(round(decimal, 2)))
                    except:
                        self.logger.warn("name: " + name + " does not have a price.")
                        price = -1

                    daily_percent_change = daily_percent_change.replace('"', '')


                    if float(price) > 0:
                        new_json[key] = {"name": str(name), "price": price, "daily_price_change": daily_price_change,
                                         "daily_percent_change": daily_percent_change,
                                         "day_open": day_open,
                                         "day_high": day_high,
                                         "day_low": day_low,
                                         "market_cap": market_cap,
                                         "pe_ratio": pe_ratio,
                                         "div_yield": div_yield,
                                         }
                except ValueError as e:
                    self.logger.exception("Error while adding a stock to the new cache.\n" +
                                          "key: " + str(key) + "\n" +
                                          "name: " + str(name) + "\n" +
                                          "line: " + str(line))
                    #TODO remove that stock from parsed_symbols.json
                    continue
        except Exception:
            self.logger.exception("Error calling YahooStockAPI, loading stock data from a backup source")
            self.load_from_file_path = './static/cache.json' #TODO remove this when self.load_cache_from_file() is removed
            self.load_cache_from_file() #TODO Remove this later..should not be in production, find backup sources

    def get_stock_prices(self, symbols):
        """
        Returns stock prices (as strings) that are delimited by newlines ("\n").

        symbols - an array of symbols whose stock prices will be returned
        """
        self.logger.info("Retrieving stock prices for the following symbols: " + str(symbols))
        prices = ''
        for i, symbol in enumerate(symbols):
            info = self.parsed_json.get(symbol)
            if not info:
                self.logger.warning("Stock symbol " + str(symbol) + " not found")
                return None
            price = info.get("price")
            if not price:
                self.logger.error("No price found for an existing symbol. This should not happen and "
                                  "needs investigation")
            if i == len(symbols) - 1:
                prices += price
            else:
                prices += price + '\n'
        return prices

    def get_stock_price(self, symbol):
        try:
            return self.parsed_json[symbol]["price"]
        except KeyError, e:
            self.logger.exception("Stock symbol " + str(symbol) + " was not found in the cache")
            raise e
    
    def load_cache_from_file(self):
        # cache_path = './static/cache.json'
        cache_path = self.load_from_file_path
        self.logger.info("Loading cache from file: " + str(cache_path))
        cache_file = open(cache_path, 'r')
        json_string = ''
        for line in cache_file:
            json_string += line
        
        new_json = json.loads(json_string)
        new_json['last_updated'] = str(datetime.datetime.utcnow().isoformat())
        self.parsed_json = new_json
