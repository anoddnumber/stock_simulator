from data_retriever import DataRetriever
from utility import do_every
from cache2 import Cache2
import time


class CacheUpdater:

    def __init__(self, cache, options, symbols, output_file=None):
        """
        Updates the cache given to it on a periodic basis

        :param cache: the cache to update
        :param options: list of options
        :param symbols: list of stock symbols
        :param output_file: optional, prints out results to a file
        """
        self.cache = cache
        self.options = options
        self.symbols = symbols
        self.output_file = output_file
        self.timer = None

    def start_updates(self, time_interval=-1):
        """
        Updates the cache once every time_interval

        :param time_interval: Number of seconds to wait until updating again
        """
        if time_interval > 0:
            self.timer = do_every(time_interval, self.update)
        else:
            raise Exception("time_interval must be a positive number, current value: " + str(time_interval))

    def update(self):
        results = DataRetriever.get_data(self.symbols, self.options)
        self.cache.store(results)

        if self.output_file is not None:
            self.cache.save_to_file(self.output_file)

    def stop_updates(self):
        if self.timer is not None:
            self.timer.cancel()

if __name__ == '__main__':
    cache = Cache2()
    updater = CacheUpdater(cache, ['l1', 'c1'], ['MSFT', 'AMZN'], './static/cache2.json')
    updater.start_updates(10)
    time.sleep(15)