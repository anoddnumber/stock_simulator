Stock Simulator Project

Uses Python 2.7, Flask, HTML5, Javascript, CSS, MongoDB, and Bootstrap (uses Grunt and NodeJS).


#Developer Information
Install Python 2.7 (not Python 3, although it may still work), PyMongo (3.0.3+), MongoDB (3.0.6+), Flask (0.10.1+), Bootstrap (3.3.6+), Grunt (0.1.13+), NodeJS (v4.2.2). 

While not necessary, installing the Flask-DebugToolbar will be very useful for developers: https://pypi.python.org/pypi/Flask-DebugToolbar

The project has a single HTML file called index.html. The reason we only have a single HTML file is because we want the user to have a very fast and smooth experience. The user will not have to load new pages (which can be slow) but rather stay on the same page but reveal and hide different elements. This is acheived with Javascript/CSS.



Furthermore, when the user loads the initial page, the page makes a single AJAX call to the server, asking for stock information. This is stored in the variable stockSymbolsMap in stock_table_methods.js. This variable should be where the client gets all the information from. The keys are stock symbols and the values are objects with keys "name" and "price". Thus, the client stores this map as a cache which can be accessed very quickly. Currently, there is no way for this map to get refereshed without reloading the page, this will be added later.

On the server side, there is a file called app.py which is the entry point for the server. It contains the services we offer and their URIs (like /info).

For this project, we need the following data: A list of possible stock symbols and their respective names, their current stock prices, and their historical stock prices. We currently do not have historical stock price data.

For the list of stock symbols and names, we retreive a text file (nasdaqlisted.txt) from NASDAQ. (ftp://ftp.nasdaqtrader.com/symboldirectory/) Currently, we just use a single copy from August 28, 2015. NASDAQ maintains the list and updates it every night. Retreiving this file daily will be a later task. With this file, we parse it using parse_stock_symbol_file.py, a script to format the data into a .json file called parsed_symbols.json. The keys are the stock symbols and the values are the stock names.

To retreive stock prices, we use Yahoo's Finance API. It is documented here: http://www.jarloo.com/yahoo_finance/. The API has a limit of 200 symbols per call. It was also ban you if you call it too fast. Thus, the server keeps a cache called cache.json. The cache gets updated by calling Yahoo's API whenever the server gets a call for stock information (/info or /stockSymbolsMap) and it has not been more than 15 minutes since the last update. This logic may need to be upgraded in the future to always have the most up to date stock prices. cache.json contains a last_updated key which contains the last time it has been updated using Yahoo's API.

