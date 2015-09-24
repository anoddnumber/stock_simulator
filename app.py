from py.yahoo_stock_api import YahooStockAPI
from flask import Flask, session, send_from_directory, request, jsonify
from py.db_access import DbAccess, UsersDbAccess
from py.user import User
from py.invalid_usage import InvalidUsage
from py.cache import Cache
import json
from jinja2 import Environment, PackageLoader
import cgi


env = Environment(loader=PackageLoader('py', 'templates'))
app = Flask(__name__, static_url_path='')
app.secret_key='i\xaa:\xee>\x90g\x0e\xf0\xf6-S\x0e\xf9\xc9(\xde\xe4\x08*\xb4Ath'
cache = Cache()
config = {'defaultCash' : 50000}

"""
The root page. There is only 1 html page in this project.
Everything else is a service.
"""
@app.route("/", methods=['GET'])
def root():
    username = session.get('username')
    cash = ''
    
    print username
    if username is None:
        username = "Not logged in"
    else:
        user = userDbAccess.getUserByUsername(username)
        if user is None:
            username = "Not logged in"
        else:
            cash = str(user.getRoundedCash())
    
    username = cgi.escape(username)
    template = env.get_template('index.html')
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
def getStockInfo():
    symbols = request.args.get('symbols')
    if symbols == None:
        return 'No symbols were in the get request'
    return getStockInfoHelper([x.strip() for x in symbols.split(',')])

"""
Returns stock prices that are delimited by newlines ("\n").

symbols - an array of stock symbols (that are strings)
"""
def getStockInfoHelper(symbols):
    if symbols == None:
        return None
    cache.update(5)
    return cache.getStockPrices(symbols)

"""
This service returns a json formatted string whose keys are available stock symbols
and whose values are the stock symbols' names and prices.

TODO: retreive the NASDAQ file daily (currently called stock_symbols.txt) and generate the json file daily (currently called parsed_symbols.json).
"""
@app.route("/stockSymbolsMap", methods=['GET'])
def getStockSymbolMap():
    print "getStockSymbolMap"
    cache.update(5)
    return json.dumps(cache.parsed_json, sort_keys=True)

"""
This service creates an account for the user.
It takes in a username, password and email, does verfications, and saves the information to the database
or raises an error if there is an issue.
"""
@app.route("/createAccount", methods=['POST'])
def createAccount():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    print username
    print password
    print email
    print "createAccount()"
    
    dict = {'username' : username, 'password' : password, 'email' : email, 'cash' : config.get('defaultCash')}
    user = User(dict)
    return userDbAccess.createUser(user)

"""
Logs the user in. Verifies that the given username and password match the ones in the database.
TODO: Cookies
"""
@app.route("/login", methods=['POST'])
def login():
    print 'login'
    username = request.form['username']
    password = request.form['password']
    user = userDbAccess.getUserByUsername(username)
    if not user:
        raise InvalidUsage('Wrong username or password', status_code=400)
    
    if password == user.password:
        print 'Username and password match'
    else:
        print 'Wrong password'
        raise InvalidUsage('Wrong username or password', status_code=400)
    
    session['username'] = username
    return "Logged in"

"""
Logs the user out.
"""
@app.route("/logout", methods=['POST'])
def logout():
    session.pop('username', None)
    return "Logged out"

@app.route("/buyStock", methods=['POST'])
def buyStock():
    #get stock symbol
    #get username from session/cookie
    #get number of stocks that want to be purchased
    username = session.get('username')
    if username is None:
        return 'Not logged in, cannot buy stock.'
    user = userDbAccess.getUserByUsername(username)
    symbol = request.form['symbol']
    quantity = request.form['quantity']
    stockPrice = request.form['stockPrice']
    
    return None

"""
"""
@app.route("/getUserInfo", methods=['GET'])
def getUserInfo():
    username = session.get('username')
    if username is None:
        return 'Not logged in, cannot retreive information.'
    user = userDbAccess.getUserByUsername(username)
    dict = {'cash' : user.getRoundedCash()}
    return json.dumps(dict, sort_keys=True)

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
    dbAccess = DbAccess("stock_market_simulator_db")
    userDbAccess = UsersDbAccess(dbAccess)
    app.debug = True
    app.run()
