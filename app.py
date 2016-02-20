import json
import cgi
import time

from flask import Flask, session, redirect, request, jsonify, url_for
from jinja2 import Environment, PackageLoader
from flask_debugtoolbar import DebugToolbarExtension

from py.db_access import UsersDbAccess
from py.user import User
from py.exceptions.invalid_usage import InvalidUsage
from py.cache import Cache
from py.exceptions.create_account_errors import *

env = Environment(loader=PackageLoader('py', 'templates'))
app = Flask(__name__, static_url_path='')
app.secret_key='i\xaa:\xee>\x90g\x0e\xf0\xf6-S\x0e\xf9\xc9(\xde\xe4\x08*\xb4Ath'
cache = Cache()
config = {'defaultCash' : 50000}

"""
The root page where the user logs into the application
"""
@app.route("/", methods=['GET'])
def root():
    username = session.get('username')
    print username
    if username is None:
        template = env.get_template('index.html')
        return template.render()
    else:
        return redirect(url_for('the_app'))

"""
Returns a page where the user can buy/sell stocks as well as information regarding the stock.
"""
@app.route("/stockInfo", methods=['GET'])
def stock_info():
    symbol = cgi.escape(request.args.get('symbol'))
    price = get_stock_info_helper([symbol])

    template = env.get_template('stock_info_page.html')
    return template.render(symbol=symbol, price=price)

"""
The application. Redirects to the root page if the user is not logged in.
"""
#TODO change names
@app.route("/theApp", methods=['GET'])
def the_app():
    username = session.get('username')

    print username
    if username is None:
        return redirect(url_for('root'))
    else:
        user = UsersDbAccess.get_user_by_username(username)
        if user is None:
            session.pop('username', None)
            return redirect(url_for('root'))
        else:
            cash = str(user.getRoundedCash())

    username = cgi.escape(username)
    template = env.get_template('simulator.html') #TODO change name
    return template.render(username=username, cash=cash)

"""
Gets the stock prices of the passed in symbols.
The client includes a symbols argument containing a string of stock symbols
which the client wants the prices of. The symbols are delimited by commas (",").
For example, symbols="AMZN,AAPL,GOOG" would be correct.

The service has a cache where it looks for the data.
The method attempts to update the cache every time it is called.
The cache will update if it has been more than n minutes since it has updated (specified in the argument, currently 15 minutes).
The stock prices will be returned in the same order as the arguments, delimited by newlines ("\n").
"""
@app.route("/info", methods=['GET'])
def get_stock_info():
    symbols = request.args.get('symbols')
    if symbols is None:
        return 'No symbols were in the get request'
    return get_stock_info_helper([x.strip() for x in symbols.split(',')])

"""
Returns stock prices that are delimited by newlines ("\n").

symbols - an array of stock symbols (that are strings)
"""
def get_stock_info_helper(symbols):
    if symbols is None:
        return None
    cache.update(5)
    return cache.getStockPrices(symbols)

"""
This service returns a json formatted string whose keys are available stock symbols
and whose values are the stock symbols' names and prices.

TODO: retrieve the NASDAQ file daily (currently called stock_symbols.txt) and generate the json file daily (currently called parsed_symbols.json).
"""
@app.route("/stockSymbolsMap", methods=['GET'])
def get_stock_symbol_map():
    print "getStockSymbolMap"
    seconds_left = cache.update(5)

    lenient_time = 2 #give extra time for the server to update before the client calls again
    delay = seconds_left + lenient_time

    info_dict = {'stockSymbolsMap' : cache.json, 'delay' : delay * 1000}
    time.sleep(5)
    return jsonify(info_dict)

"""
This service creates an account for the user.
It takes in a username, password and email, does verifications, and saves the information to the database
or raises an error if there is an issue.
"""
@app.route("/createAccount", methods=['POST'])
def create_account():
    username = request.form['username']
    password = request.form['password']
    retype_password = request.form['retypePassword']
    email = request.form['email']

    #TODO remove print statements
    print "create_account()"
    print "username: " + str(username)
    print "email: " + str(email)
    print "password: " + str(password)
    print "retype password: " + str(retype_password)

    if password is not retype_password:
        template = env.get_template('index.html')
        return template.render(createAccountError='Passwords do not match.')

    user_dict = {'username' : username,
                'password' : password,
                'email' : email,
                'cash' : config.get('defaultCash'),
                'stocks_owned' : {} }
    user = User(user_dict)

    try:
        UsersDbAccess.create_user(user)
    except DuplicateUsernameError:
        template = env.get_template('index.html')
        return template.render(createAccountError='Username already taken.')
    except DuplicateEmailError:
        template = env.get_template('index.html')
        return template.render(createAccountError='Email already taken.')
    session['username'] = user.username
    return redirect(url_for('the_app'))

"""
Logs the user in. Verifies that the given username and password match the ones in the database.
TODO: Cookies
"""
@app.route("/login", methods=['POST'])
def login():
    print 'login'
    print "request: " + str(request)
    email = request.form['email']
    user = UsersDbAccess.get_user_by_email(email)

    password = request.form['password']
    if not user:
        print 'User does not exist'
        template = env.get_template('index.html')
        return template.render(loginError='Email and password do not match up.')

    if user.check_password(password):
        print 'Username and password match'
    else:
        print 'Wrong password'
        template = env.get_template('index.html')
        return template.render(loginError='Email and password do not match up.')

    #session.pop('username', None) #this probably isn't needed..
    session['username'] = user.username
    return redirect(url_for('the_app'))

"""
Logs the user out.
"""
@app.route("/logout", methods=['POST'])
def logout():
    print 'logout'
    session.pop('username', None)
    return redirect(url_for('root'))


@app.route("/buyStock", methods=['POST'])
def buy_stock():
    print 'buyStock'
    
    username = session.get('username')
    if username is None:
        return 'Not logged in, cannot buy stock.'
    
    user = UsersDbAccess.get_user_by_username(username)
    if user is None:
        return 'User with username ' + username + ' not found in database.'

    try:
        symbol = request.form['symbol']
        quantity = int(request.form['quantity'])
        stock_price = float(request.form['stockPrice'])
    except ValueError:
        return "Error reading arguments"
    
    if symbol is None or quantity is None or stock_price is None:
        return 'Missing at least one argument: symbol, quantity, stockPrice required. No optional arguments.'

    # check if the price that the user wants to buy the stock for is the same as the server's stock price
    stocks_map = cache.json
    symbol_map = stocks_map.get(symbol)
    if symbol_map is None:
       return "Invalid symbol"
    server_stock_price = float(symbol_map.get("price"))

    if stock_price != server_stock_price:
       return "Stock price changed, please try again."
    
    # check if quantity is a positive integer
    if stock_price < 0 or quantity < 0:
        return "stock price or quantity less than 0"
        
    total_cost = quantity * stock_price
    # check that the user has enough cash to buy the stocks requested
    if total_cost >= user.cash:
        return "Not enough cash"
    
    # buy the stock
    return UsersDbAccess.addStockToUser(user.username, symbol, stock_price, quantity)


@app.route("/sellStock", methods=['POST'])
def sell_stock():
    username = session.get('username')
    if username is None:
        return 'Not logged in, cannot sell stock.' 
    
    user = UsersDbAccess.get_user_by_username(username)
    if user is None:
        return 'User with username ' + username + ' not found in database.'

    try:
        symbol = request.form['symbol']
        quantity = int(request.form['quantity'])
        stock_price = float(request.form['stockPrice'])
    except ValueError, e:
        return "Error reading arguments"
    
    if symbol is None or quantity is None or stock_price is None:
        return 'Missing at least one argument: symbol, quantity, stockPrice required. No optional arguments.'

    stocks_map = cache.json
    symbol_map = stocks_map.get(symbol)
    if symbol_map is None:
        return "Invalid symbol"
    server_stock_price = float(symbol_map.get("price"))

    if stock_price < 0 or quantity < 0:
        return "stock price or quantity less than 0"

    if stock_price != server_stock_price:
        return "Stock price changed, please try again."

    # sell the stock
    return UsersDbAccess.sell_stocks_from_user(username, symbol, quantity, cache)

@app.route("/getUserInfo", methods=['GET'])
def get_user_info():
    username = session.get('username')
    if username is None:
        return 'Not logged in, cannot retrieve information.'
    user = UsersDbAccess.get_user_by_username(username)
    if user is None:
        return 'Could not find the current user in the database.'
    user_dict = {'cash' : user.getRoundedCash(), 'stocks_owned' : user.stocks}
    return json.dumps(user_dict, sort_keys=True)

"""
This method is used to send error messages to the client.
Whenever an InvalidUsage is raised, this method will be executed.
"""
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
            
if __name__ == "__main__":
    app.debug = True
    toolbar = DebugToolbarExtension(app)
    app.run()
