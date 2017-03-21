from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from cache2 import Cache2
from cache_updater import CacheUpdater
from stock_symbols import StockSymbols
from data_retriever import DataOptions

import logging
import logging_setup
import os


app = Flask(__name__, static_url_path='', template_folder='py/templates')

if __name__ == "__main__":
    # set up logging
    logging_setup.setup()

    # set app.debug to True for the debug toolbar to appear
    app.debug = False
    toolbar = DebugToolbarExtension(app)

    # the cache will hold stock data
    cache = Cache2()

    # determines what type of information we should get
    stock_options = [DataOptions.LAST_TRADE_PRICE, DataOptions.CHANGE, DataOptions.CHANGE_IN_PERCENT,
                     DataOptions.OPEN, DataOptions.DAY_HIGH, DataOptions.DAY_LOW, DataOptions.MARKET_CAPITALIZATION,
                     DataOptions.P_E_RATIO, DataOptions.DIVIDEND_YIELD]

    # symbols that are in the cache
    stock_symbols = StockSymbols.get_symbols()

    # update the cache every 15 minutes
    cache_updater = CacheUpdater(cache, stock_options, stock_symbols, './static/cache2.json')
    cache_updater.start_updates(15 * 60)

    # Bind to PORT if defined, otherwise default to 5000.
    # Heroku will define the PORT environment variable, so use it if it is defined
    port = int(os.environ.get('PORT', 5000))

    logger = logging.getLogger(__name__)
    logger.info("Starting server")
    # run_simple('localhost', port, app, ssl_context=('./ssl_key.crt', './ssl_key.key'))  # use HTTPS in devo

    # host='0.0.0.0' tells your operating system to listen on all public IPs.
    app.run(host='0.0.0.0', port=port)
    # app.run()