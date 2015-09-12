from py.yahoo_stock_api import YahooStockAPI
from flask import Flask, send_from_directory, request, jsonify
from py.db_access import DbAccess, UsersDbAccess
from py.user import User
from py.invalid_usage import InvalidUsage
from py.cache import Cache
import json

app = Flask(__name__, static_url_path='')
cache = Cache()

"""
The root page. There is only 1 html page in this project.
Everything else is a service.
"""
@app.route('/')
def root():
    return app.send_static_file('index.html')

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
@app.route("/info")
def getStockInfo():
    symbols = request.args.get('symbols')
    if symbols == None:
        return 'No symbols were in the get request'
    return getStockInfoHelper([x.strip() for x in symbols.split(',')])
    
def getStockInfoHelper(symbols):
    if symbols == None:
        return None
    cache.update(15)
    return cache.getStockPrices(symbols)

"""
This service returns a json formatted file whose keys are available stock symbols
and whose values are the stock symbols' names.

The json file is generated from a file taken from NASDAQ (Which is updated daily).
For more information on the file, visit the Wiki page on Github.

TODO: retreive the NASDAQ file daily (currently called stock_symbols.txt) and generate the json file daily (currently called parsed_symbols.json).
"""
@app.route("/stockSymbolsMap", methods=['GET'])
def getStockSymbolMap():
    print "getStockSymbolMap"
    cache = open('./static/parsed_symbols.json', 'r')
    json_string = ''
    for line in cache:
        json_string += line
    parsed_json = json.loads(json_string)
    keys = parsed_json.keys()
    keys.sort()
    prices = getStockInfoHelper(keys).split('\n', len(keys)-1)
    for i, price in enumerate(prices):
        obj = str('{"name":"' + str(parsed_json[keys[i]]) + '","price":"' + str(price) + '"}')
        parsed_json[keys[i]] = obj
    return json.dumps(parsed_json, sort_keys=True)

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
    user = User(username, password, email)
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
        
    return "Login"

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
