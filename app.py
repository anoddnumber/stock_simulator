from py.yahoo_stock_api import YahooStockAPI
from flask import Flask, send_from_directory, request, jsonify
from py.db_access import DbAccess, UsersDbAccess
from py.user import User
from py.invalid_usage import InvalidUsage
from py.cache import Cache

app = Flask(__name__, static_url_path='')
cache = Cache()

@app.route('/')
def root():
    return app.send_static_file('index.html')
    
@app.route("/info")
def getStockInfo():
    cache.update(15)
    
    symbols = request.args.get('symbols')
    if symbols == None:
        return 'No symbols were in the get request'
    symbols = [x.strip() for x in symbols.split(',')]
    return cache.getStockPrices(symbols)

@app.route("/stockSymbolsMap", methods=['GET'])
def getStockSymbolMap():
    print "getStockSymbolMap"
    return app.send_static_file('parsed_symbols.json')

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
