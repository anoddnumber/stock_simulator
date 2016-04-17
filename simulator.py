import json
import cgi
import time

from flask import Flask, redirect, request, jsonify, url_for, g, current_app
from jinja2 import Environment, PackageLoader
from flask_debugtoolbar import DebugToolbarExtension

from py.db_access import UsersDbAccess
from py.exceptions.invalid_usage import InvalidUsage
from py.cache import Cache
from werkzeug.serving import run_simple

import py.logging_setup
import logging
from flask_mongoengine import MongoEngine
from py.db_info import DBInfo
from flask_security import Security, MongoEngineUserDatastore, login_user, \
    current_user, login_required
from flask_mail import Mail
from flask_security.utils import encrypt_password
from flask_security.confirmable import send_confirmation_instructions
from py.user import User, Role
from py.extended_register_form import ExtendedRegisterForm

env = Environment(loader=PackageLoader('py', 'templates'))
app = Flask(__name__, static_url_path='', template_folder='py/templates')
app.secret_key = 'i\xaa:\xee>\x90g\x0e\xf0\xf6-S\x0e\xf9\xc9(\xde\xe4\x08*\xb4Ath'

# MongoDB Config
app.config['MONGODB_DB'] = DBInfo.db_name
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = DBInfo.db_port
app.config['SECURITY_PASSWORD_SALT'] = 'Zafaw9rtnisO9QCIi7ekdGNFu4cbIjtedzhWmMwebLE='
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'

# Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'theofficialstockmeister'
app.config['MAIL_PASSWORD'] = 'testaccount'

# Flask-Security general config
app.config['SECURITY_CONFIRMABLE'] = True  # the user must confirm their account through email
app.config['SECURITY_EMAIL_SENDER'] = 'Stock Meister <this_email_is_ignored@gmail.com>'
app.config['WTF_CSRF_ENABLED'] = False  # use for debugging to be able to send requests over rest client

# Flask-Security URL configs
app.config['SECURITY_LOGIN_URL'] = '/login'
app.config['SECURITY_POST_LOGIN_VIEW'] = '/'
app.config['SECURITY_POST_REGISTER_VIEW'] = '/post_register'

# Flask-Security register configs
app.config['SECURITY_REGISTERABLE'] = True

# Flask-Security login error messages
app.config['SECURITY_MSG_CONFIRMATION_REQUIRED'] = ('Please confirm your account through your email.', 'error')
app.config['SECURITY_MSG_EMAIL_NOT_PROVIDED'] = ('Email or password is incorrect.', 'error')
app.config['SECURITY_MSG_PASSWORD_NOT_PROVIDED'] = ('Email or password is incorrect.', 'error')
app.config['SECURITY_MSG_USER_DOES_NOT_EXIST'] = ('Email or password is incorrect.', 'error')
app.config['SECURITY_MSG_PASSWORD_NOT_SET'] = ('Unexpected error.', 'error')
app.config['SECURITY_MSG_INVALID_PASSWORD'] = ('Email or password is incorrect.', 'error')
app.config['SECURITY_MSG_DISABLED_ACCOUNT'] = ('This account is disabled.', 'error')

config = {'defaultCash': 50000}
db = MongoEngine(app)
user_datastore = MongoEngineUserDatastore(db, User, Role)
# security = Security(app, user_datastore, register_blueprint=False)
security = Security(app, user_datastore, confirm_register_form=ExtendedRegisterForm)
mail = Mail(app)

# security.app.login_manager.login_view = 'root' # this will give a ?next= in the URL.
# Using the unauthorized handler will give more control, we can add the next parameter later


@security.app.login_manager.unauthorized_handler
def unauthorized_callback():
    list_routes()
    return redirect(url_for('security.login'))


@app.route("/", methods=['GET'])
@login_required
def root():
    """
    The actual application
    """
    list_routes()  # for debugging

    logger.info("User with IP address " + str(request.remote_addr) + " has visited.")
    template = env.get_template('simulator.html')
    return template.render()


@security.context_processor
def security_global_context_processor():
    def get_form_error(form):
        for field in form:
            try:
                if len(field.errors) > 0:
                    return field.errors[0]
            except AttributeError:
                continue
        return None
    return dict(get_form_error=get_form_error)


@app.route("/site-map")
def site_map():
    return str(list_routes())


def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print line

    return output

# """
# Returns a page where the user can buy/sell stocks as well as information regarding the stock.
# """
# @app.route("/stockInfo", methods=['GET'])
# def stock_info():
#     symbol = cgi.escape(request.args.get('symbol'))
#     price = get_stock_info_helper([symbol])
#
#     logger.info("Retrieving information for stock with symbol " + str(symbol) +
#                 "and price " + str(price))
#
#     template = env.get_template('stock_info_page.html')
#     return template.render(symbol=symbol, price=price)

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
@login_required
def get_stock_info():
    symbols = request.args.get('symbols')
    logger.info("Retrieving information for stock symbols " + str(symbols))
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
    return cache.get_stock_prices(symbols)

"""
This service returns a json formatted string whose keys are available stock symbols
and whose values are the stock symbols' names and prices.

TODO: retrieve the NASDAQ file daily (currently called stock_symbols.txt) and generate the json file daily (currently called parsed_symbols.json).
"""
@app.route("/stockSymbolsMap", methods=['GET'])
@login_required
def get_stock_symbol_map():
    logger.info("Retrieving the stockSymbolsMap")
    seconds_left = cache.update(5)

    lenient_time = 2 # give extra time for the server to update before the client calls again
    delay = seconds_left + lenient_time

    info_dict = {'stockSymbolsMap' : cache.json, 'delay' : delay * 1000}

    # time.sleep(5)
    return jsonify(info_dict)


# """
# This service creates an account for the user.
# It takes in a username, password and email, does verifications, and saves the information to the database
# or raises an error if there is an issue.
# """
# @app.route("/createAccount", methods=['POST'])
# def create_account():
#     username = request.form['username'].strip()
#     password = request.form['password']
#     retype_password = request.form['retypePassword']
#     email = request.form['email'].strip()
#
#     # if statement for unit tests to bypass recaptcha
#     # if not config.get("DEBUG"):
#     #     captcha = request.form['g-recaptcha-response']
#     #
#     #     logger.info("captcha: " + str(captcha))
#     #     data = urllib.urlencode({'secret' : '6Lf7ZBoTAAAAAHIKbm4AnecJxycyM5PIjmWt3eO_',
#     #                          'response'  : captcha})
#     #     u = urllib2.urlopen('https://www.google.com/recaptcha/api/siteverify', data)
#     #     google_response = u.read()
#     #     logger.info("Google responded to captcha with " + str(google_response))
#     #
#     #     google_json = json.loads(google_response)
#     #     logger.info('google_json.get("success"): ' + str(google_json.get("success")))
#     #
#     #     if not google_json.get("success"):
#     #         logger.warning("User tried creating an account but failed because reCaptcha failed")
#     #         template = env.get_template('index.html')
#     #         return template.render(createAccountError='Failed to create an account, please try again.')
#
#     if username == "" or password == "" or email == "":
#         logger.warning("User tried to create account with either a blank username, password, or email")
#         template = env.get_template('index.html')
#         return template.render(createAccountError='Invalid username, password, or email.')
#
#     if " " in username:
#         logger.warning("User tried to create an account with a space in it.")
#         template = env.get_template('index.html')
#         return template.render(createAccountError='Username cannot contain spaces.')
#
#     logger.info("User trying to create an account with username " + str(username) +
#                  " and email " + str(email))
#
#     # Use != instead of "is not" since we are comparing unicode, not strings
#     if password != retype_password:
#         logger.info("User tried creating an account but failed because passwords didn't match")
#         template = env.get_template('index.html')
#         return template.render(createAccountError='Passwords do not match.')
#
#     encrypted_password = encrypt_password(password)
#     print "encrypted_password: " + str(encrypted_password)
#
#     user_dict = {
#                 'username': username,
#                 'password': encrypted_password,
#                 'email': email,
#                 'cash': config.get('defaultCash'),
#                 'stocks_owned': {}
#                  }
#     user = User(**user_dict)
#
#     if users_db_access.get_user_by_username(username):
#         logger.info("User tried creating an account but failed because username " + str(username) + " already exists")
#         template = env.get_template('index.html')
#         return template.render(createAccountError='Username already taken.')
#     elif users_db_access.get_user_by_email(email):
#         logger.info("User tried creating an account but failed because " + str(email) + " already exists")
#         template = env.get_template('index.html')
#         return template.render(createAccountError='Email already taken.')
#     else:
#         user = users_db_access.create_user(user)
#
#     # login_user(user)
#
#     logger.info("Sending email to user " + str(username) + " with email address " + str(email) +
#                 " because he/she created an account.")
#
#     send_confirmation_instructions(user)
#
#     # return redirect(url_for('root'))
#     return "created account"

# """
# Logs the user in. Verifies that the given username and password match the ones in the database.
# TODO: Cookies
# """
# @app.route("/login", methods=['POST'])
# def login():
#     email = request.form['email']
#     password = request.form['password']
#
#     user = users_db_access.get_user_by_email(email)
#     logger.info("User: " + str(user) + " tried logging in")
#
#     if not user:
#         logger.info("User tried logging in with email " + str(email) + " but failed because no user exists for the email")
#         template = env.get_template('index.html')
#         return template.render(loginError='Email and password do not match up.')
#
#     if user.check_password(password):
#         remember_me = str(request.form.get('remember-me')) == "true"
#         logger.info("Password matches, login successful. Remember me: " + str(remember_me))
#         login_user(user, remember_me)
#     else:
#         logger.info("Login failed, password incorrect.")
#         template = env.get_template('index.html')
#         return template.render(loginError='Email and password do not match up.')
#
#     return redirect(url_for('root'))


@app.route("/post_register", methods=['GET'])
def post_register():
    """
    The view that is shown to the user after they create a new account. The user will still have to
    confirm their email address
    """
    # logout_user()
    # return redirect(url_for('root'))
    template = env.get_template('post_register.html')
    return template.render()


# """
# Logs the user out.
# """
# @app.route("/logout", methods=['POST'])
# def logout():
#     print "blah"
#     print str(request.form.get('abc'))
#     print "request.json: " + str(request.json)
#     # logout_user()
#     # return redirect(url_for('root'))
#     return "hi"


@app.route("/buyStock", methods=['POST'])
@login_required
def buy_stock():
    username = current_user.username

    try:
        symbol = request.form['symbol']
        quantity = int(request.form['quantity'])
        stock_price = float(request.form['stockPrice'])

    except ValueError:
        logger.warning("User trying to buy stock but there was an error trying to read the arguments")
        return "Error reading arguments"
    
    if symbol is None or quantity is None or stock_price is None:
        logger.warning("Missing argument when buying stock:\n" +
                       "symbol: " + str(symbol) + ", " +
                       "quantity: " + str(quantity) + ", " +
                       "stock_price: " + str(stock_price))
        return 'Missing at least one argument: symbol, quantity, stockPrice required. No optional arguments.'

    # check if the price that the user wants to buy the stock for is the same as the server's stock price
    stocks_map = cache.json
    symbol_map = stocks_map.get(symbol)
    if symbol_map is None:
        logger.warning("User tried to buy stock with symbol " + str(symbol) + " but is not in the stocks map")
        return "Invalid symbol"
    server_stock_price = float(symbol_map.get("price"))

    # check if the passed in stock price and quantity are positive
    if stock_price <= 0 or quantity <= 0:
        logger.warning("The stock price is either less than or equal to 0 or the user tried to zero or fewer amount of stock")
        logger.warning("stock_price: " + str(stock_price) + ", quantity: " + str(quantity))
        return "Stock price or quantity less than 0"

    if stock_price != server_stock_price:
        logger.warning("User tried to buy the stock at price " + str(stock_price) + " but the server stock price was " + str(server_stock_price))
        return "Stock price changed, please try again."

    total_cost = quantity * stock_price
    # check that the user has enough cash to buy the stocks requested
    if total_cost >= current_user.cash:
        logger.warning("User " + str(username) + " tried to buy more stocks than he/she can afford")
        logger.warning("total_cost: " + str(total_cost) + ", user.cash: " + str(current_user.cash))
        return "Not enough cash"

    logger.info("User " + str(username) + " passed all validation for buying " + str(quantity) + " stocks with symbol " + str(symbol) +
               " at a stock price of " + str(stock_price) + ", totaling a cost of " + str(total_cost))
    # buy the stock
    return users_db_access.add_stock_to_user(username, symbol, stock_price, quantity)

@app.route("/sellStock", methods=['POST'])
@login_required
def sell_stock():
    username = current_user.username

    try:
        symbol = request.form['symbol']
        quantity = int(request.form['quantity'])
        stock_price = float(request.form['stockPrice'])
    except ValueError:
        logger.warning("User trying to sell stock but there was an error trying to read the arguments")
        return "Error reading arguments"
    
    if symbol is None or quantity is None or stock_price is None:
        logger.warning("Missing argument when selling stock:\n" +
                       "symbol: " + str(symbol) + ", " +
                       "quantity: " + str(quantity) + ", " +
                       "stock_price: " + str(stock_price))
        return 'Missing at least one argument: symbol, quantity, stockPrice required. No optional arguments.'

    stocks_map = cache.json
    symbol_map = stocks_map.get(symbol)
    if symbol_map is None:
        logger.warning("User tried to sell stock with symbol " + str(symbol) + " but is not in the stocks map")
        return "Invalid symbol"
    server_stock_price = float(symbol_map.get("price"))

    if stock_price < 0 or quantity < 0:
        logger.warning("User with username " + str(username) + " tried to sell a negative amount of stock or for a negative price")
        logger.warning("stock_price: " + str(stock_price) + ", quantity: " + str(quantity))
        return "Stock price or quantity less than 0"

    if stock_price != server_stock_price:
        logger.warning("User tried to sell the stock at price " + str(stock_price) + " but the server stock price was " + str(server_stock_price))
        return "Stock price changed, please try again."

    logger.info("User with username " + str(username) + " passed all validations for selling " + str(quantity) + " stocks with symbol " + str(symbol) +
               " at a stock price of " + str(stock_price))
    # sell the stock
    return users_db_access.sell_stocks_from_user(username, symbol, quantity, cache)


@app.route("/getUserInfo", methods=['GET'])
@login_required
def get_user_info():
    user_dict = {'cash': str(current_user.cash), 'stocks_owned': current_user.stocks_owned}
    logger.info("Returning user information for " + str(current_user.username))
    logger.info("user_dict: " + str(user_dict))
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

def init_logger():
    global logger
    py.logging_setup.setup()
    logger = logging.getLogger(__name__)


def init_db():
    global users_db_access
    users_db_access = UsersDbAccess(user_datastore)


def init_cache(cache_path=None):
    global cache
    cache = Cache(cache_path)
            
if __name__ == "__main__":
    app.debug = False
    toolbar = DebugToolbarExtension(app)
    init_logger()
    init_cache()
    init_db()

    logger.info("Starting server")
    run_simple('localhost', 5000, app, ssl_context=('./ssl_key.crt', './ssl_key.key')) #use HTTPS in devo