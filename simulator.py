import json
import os
import re
import threading

from flask import Flask, redirect, request, jsonify, url_for
from jinja2 import Environment, PackageLoader
from flask_debugtoolbar import DebugToolbarExtension

from py.exceptions.invalid_usage import InvalidUsage
from py.cache import Cache
# from werkzeug.serving import run_simple

import py.logging_setup
import logging
from flask_mongoengine import MongoEngine
from py.db_info import DevoDBInfo
from flask_security import Security, current_user, login_required
from flask_mail import Mail
from py.user import User, Role
from py.extended_register_form import ExtendedRegisterForm
from py.datastores.stock_user_datastore import MongoEngineStockUserDatastore
from py.datastores.transaction_datastore import MongoEngineTransactionDatastore
from py.constants import errors, messages
from py.constants.errors import ERROR_CODE_MAP
import csv

env = Environment(loader=PackageLoader('py', 'templates'))
app = Flask(__name__, static_url_path='', template_folder='py/templates')
app.secret_key = 'i\xaa:\xee>\x90g\x0e\xf0\xf6-S\x0e\xf9\xc9(\xde\xe4\x08*\xb4Ath'

def init_logger():
    global logger
    py.logging_setup.setup()
    logger = logging.getLogger(__name__)
init_logger()

# MongoDB Config
def set_db_config():
    # split on multiple strings
    mongodb_uri = os.environ.get('MONGODB_URI')
    # mongodb_uri = 'mongodb://heroku_jnccm4lq:81b5jm0qkg0frk5j1o8bd63t84@ds021751.mlab.com:21751/heroku_jnccm4lq'
    if mongodb_uri:
        (mongo_db, db_user, db_password, host, db_port, db_name) = re.split('://|:|@|,|/', mongodb_uri)
        app.config['MONGODB_USERNAME'] = db_user
        app.config['MONGODB_PASSWORD'] = db_password
        app.config['MONGODB_HOST'] = host
        app.config['MONGODB_PORT'] = int(db_port)
        app.config['MONGODB_DB'] = db_name

        logger.info("setting db configs")
        logger.info("mongo_db: " + str(mongo_db))
        logger.info("db_user: " + db_user)
        logger.info("db_password: " + db_password)
        logger.info("host: " + str(host))
        logger.info("port: " + str(db_port))
        logger.info("db_name: " + str(db_name))
    else:
        app.config['MONGODB_DB'] = DevoDBInfo.db_name
        app.config['MONGODB_HOST'] = DevoDBInfo.host
        app.config['MONGODB_PORT'] = DevoDBInfo.db_port
set_db_config()

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
app.config['SECURITY_POST_CHANGE_VIEW'] = '/change'

# Flask-Security template paths
app.config['SECURITY_CHANGE_PASSWORD_TEMPLATE'] = 'security/change_password.html'

# Flask-Security register configs, states that there should be a registerable endpoint.
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True

# Flask-Security login error messages
app.config['SECURITY_MSG_CONFIRMATION_REQUIRED'] = ('Please confirm your account through your email.', 'error')
app.config['SECURITY_MSG_EMAIL_NOT_PROVIDED'] = ('Email or password is incorrect.', 'error')
app.config['SECURITY_MSG_PASSWORD_NOT_PROVIDED'] = ('Email or password is incorrect.', 'error')
app.config['SECURITY_MSG_USER_DOES_NOT_EXIST'] = ('Email or password is incorrect.', 'error')
app.config['SECURITY_MSG_PASSWORD_NOT_SET'] = ('Unexpected error.', 'error')
app.config['SECURITY_MSG_INVALID_PASSWORD'] = ('Email or password is incorrect.', 'error')
app.config['SECURITY_MSG_DISABLED_ACCOUNT'] = ('This account is disabled.', 'error')

config = {
    'defaultCash': 50000,
    'commission': 8.95
}
db = MongoEngine(app)
stock_user_datastore = MongoEngineStockUserDatastore(db, User, Role)
security = Security(app, stock_user_datastore, confirm_register_form=ExtendedRegisterForm)
mail = Mail(app)

# security.app.login_manager.login_view = 'root' # this will give a ?next= in the URL.
# Using the unauthorized handler will give more control, we can add the next parameter later


def get_collection():
    host = os.environ.get('MONGODB_URI')
    port = app.config['MONGODB_PORT']

    client = MongoClient(host=host,port=port)
    db_name = app.config['MONGODB_DB']
    the_db = client[db_name]
    collection = the_db[DBInfo.collection_name]
    return collection

@security.app.login_manager.unauthorized_handler
def unauthorized_callback():
    # list_routes()
    return redirect(url_for('security.login'))


@app.route("/", methods=['GET'])
@login_required
def root():
    """
    The actual application
    """
    # list_routes()  # for debugging

    logger.info("User with IP address " + str(request.remote_addr) + " has visited.")
    template = env.get_template('profile_page.html')
    return template.render(current_user=current_user, userInfo=get_user_info(),
                           stockSymbolsMap=json.dumps(cache.json), activeTab='profile')


@app.route("/stock/<symbol>", methods=['GET'])
@login_required
def stock_info_page(symbol):
    user_dict = get_user_dict()

    stocks_owned = user_dict.get("stocks_owned")
    cash = user_dict.get("cash")

    num_owned = 0
    if stocks_owned is not None:
        stock_owned_info = stocks_owned.get(symbol)
        if stock_owned_info:
            num_owned = stock_owned_info.get("total")
            if not num_owned:
                num_owned = 0
                logger.exception("User " + str(current_user) + "'s stock data is corrupted. " +
                                 "Symbol " + str(symbol) + " exists in stocks_owned but does not contain " +
                                 "a total field")
    else:
        logger.exception("Corrupted data. User " + str(current_user) + " does not have a stocks_owned field." +
                         " user_dict:" + str(user_dict) + " stocks_owned: " + str(stocks_owned))

    stock_info = cache.json.get(symbol)

    if stock_info:
        name = stock_info.get("name")  # Company name
        price = stock_info.get("price")
        daily_percent_change = stock_info.get("daily_percent_change")
        daily_price_change = stock_info.get("daily_price_change")
        day_open = stock_info.get("day_open")
        day_high = stock_info.get("day_high")
        day_low = stock_info.get("day_low")
        market_cap = stock_info.get("market_cap")
        pe_ratio = stock_info.get("pe_ratio")
        div_yield = stock_info.get("div_yield")

        if daily_price_change is not None:
            price_change = float(daily_price_change)
            if price_change > 0:
                change = 'increase'
            elif price_change < 0:
                change = 'decrease'
            else:
                change = 'same'

    if stock_info and user_dict:
        path = 'data/' + str(symbol) + '.csv'
        if os.path.isfile(path):
            with open('data/' + str(symbol) + '.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')

                info = []
                for i, row in enumerate(csv_reader):
                    if i == 0:
                        continue
                    info.append({"date": row[0], "value": row[6]})
                info.reverse()
        else:
            info = 'undefined'

        template = env.get_template('stock_info_page.html')
        return template.render(current_user=current_user, name=name, symbol=symbol, price=price, day_low=day_low,
                               daily_percent_change=daily_percent_change, daily_price_change=daily_price_change,
                               day_open=day_open, day_high=day_high, num_owned=num_owned, cash=cash, change=change,
                               commission=config['commission'], market_cap=market_cap, pe_ratio=pe_ratio,
                               div_yield=div_yield, activeTab='stocks', chartData=info)
    else:
        return "Requested stock does not exist in our database"


@app.route("/stocks", methods=['GET'])
@login_required
def stocks():
    template = env.get_template('stocks_page.html')
    return template.render(current_user=current_user, userInfo=get_user_info(),
                           stockSymbolsMap=json.dumps(cache.json), activeTab='stocks')


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


# @app.route("/site-map")
# def site_map():
#     return str(list_routes())


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


@app.route("/info", methods=['GET'])
@login_required
def get_stock_info():
    """
    Gets the stock prices of the passed in symbols.
    The client includes a symbols argument containing a string of stock symbols
    which the client wants the prices of. The symbols are delimited by commas (",").
    For example, symbols="AMZN,AAPL,GOOG" would be correct.

    The service has a cache where it looks for the data.
    The method attempts to update the cache every time it is called.
    The cache will update if it has been more than n minutes since it has updated (specified in the argument,
    currently 15 minutes).
    The stock prices will be returned in the same order as the arguments, delimited by newlines ("\n").
    """
    symbols = request.args.get('symbols')
    logger.info("Retrieving information for stock symbols " + str(symbols))
    if symbols is None:
        return 'No symbols were in the get request'
    return get_stock_info_helper([x.strip() for x in symbols.split(',')])


def get_stock_info_helper(symbols):
    """
    Returns stock prices that are delimited by newlines ("\n").

    symbols - an array of stock symbols (that are strings)
    """
    if symbols is None:
        return None
    return cache.get_stock_prices(symbols)


@app.route("/post_register", methods=['GET'])
def post_register():
    """
    The view that is shown to the user after they create a new account. The user will still have to
    confirm their email address
    """
    template = env.get_template('post_register.html')
    return template.render()


@app.route("/confirmation", methods=['GET'])
@login_required
def confirmation():
    """
    Page shown to the user after buying/selling stock
    """
    err_arg = request.args.get('err')
    error = ERROR_CODE_MAP.get(err_arg)
    active_tab = 'stocks'
    template = env.get_template('confirmation_page.html')

    if error:
        return template.render(current_user=current_user, error=error, activeTab=active_tab, err_arg=err_arg)

    try:
        last_transaction = current_user.last_transaction
        transaction_type = last_transaction['type']
        symbol = last_transaction['symbol']
        quantity = last_transaction['quantity']
        price_per_stock = last_transaction['price_per_stock']
    except KeyError:
        return template.render(current_user=current_user, error=ERROR_CODE_MAP.get(errors.UNEXP), activeTab=active_tab)

    if transaction_type == 'sell':
        message = messages.get_sell_success_message(quantity, symbol, price_per_stock)
    elif transaction_type == 'buy':
        message = messages.get_buy_success_message(quantity, symbol, price_per_stock)
    else:
        return template.render(current_user=current_user, error=ERROR_CODE_MAP.get(errors.UNEXP), activeTab=active_tab, err_arg=errors.UNEXP)

    return template.render(current_user=current_user, message=message, activeTab=active_tab)


@app.route("/buy", methods=['POST'])
@login_required
def buy_stock():
    username = current_user.username

    try:
        symbol = request.form['symbol']
        quantity = int(request.form['quantity'])
        stock_price = float(request.form['stockPrice'])

    except ValueError:
        logger.warning("User trying to buy stock but there was an error trying to read the arguments")
        return redirect(url_for('confirmation', err=errors.UNEXP))

    if symbol is None or symbol == "" or quantity is None or stock_price is None:
        logger.warning("Missing argument when buying stock:\n" +
                       "symbol: " + str(symbol) + ", " +
                       "quantity: " + str(quantity) + ", " +
                       "stock_price: " + str(stock_price))
        return redirect(url_for('confirmation', err=errors.UNEXP))

    # check if the price that the user wants to buy the stock for is the same as the server's stock price
    stocks_map = cache.json
    symbol_map = stocks_map.get(symbol)
    if symbol_map is None:
        logger.warning("User tried to buy stock with symbol " + str(symbol) + " but is not in the stocks map")
        return redirect(url_for('confirmation', err=errors.SDNE))

    server_stock_price = float(symbol_map.get("price"))

    if quantity <= 0:
        logger.info("The user tried to buy 0 or fewer stocks of " + str(symbol))
        return redirect(url_for('confirmation', err=errors.BLESS))

    # check if the passed in stock price and quantity are positive
    if stock_price <= 0:
        logger.warning("The stock price the client entered is less than or equal to 0")
        logger.warning("stock_price: " + str(stock_price) + ", quantity: " + str(quantity))
        return redirect(url_for('confirmation', err=errors.UNEXP))

    if stock_price != server_stock_price:
        logger.warning("User tried to buy the stock " + str(symbol) + " at price " + str(stock_price) +
                       " but the server stock price was " + str(server_stock_price))
        return redirect(url_for('confirmation', err=errors.PRICH))

    total_cost = quantity * stock_price + config['commission']
    # check that the user has enough cash to buy the stocks requested
    if total_cost > float(current_user.cash):
        logger.warning("User " + str(username) + " tried to buy more stocks than he/she can afford")
        logger.warning("total_cost: " + str(total_cost) + ", user.cash: " + str(current_user.cash))
        return redirect(url_for('confirmation', err=errors.BNEC))

    logger.info("User " + str(username) + " passed all validation for buying " + str(quantity) +
                " stocks with symbol " + str(symbol) + " at a stock price of " + str(stock_price) +
                ", totaling a cost of " + str(total_cost))

    # buy the stock
    rtn = stock_user_datastore.add_stock_to_user(username, symbol, stock_price, quantity)

    if rtn.get("error"):
        return redirect(url_for('confirmation', err=rtn.get("data")))
    else:
        return redirect(url_for('confirmation'))


@app.route("/sell", methods=['POST'])
@login_required
def sell_stock():
    username = current_user.username

    try:
        symbol = request.form['symbol']
        quantity = int(request.form['quantity'])
        stock_price = float(request.form['stockPrice'])
    except ValueError:
        logger.warning("User trying to sell stock but there was an error trying to read the arguments")
        return redirect(url_for('confirmation', err=errors.UNEXP))
    
    if symbol is None or symbol == "" or quantity is None or stock_price is None:
        logger.warning("Missing argument when selling stock:\n" +
                       "symbol: " + str(symbol) + ", " +
                       "quantity: " + str(quantity) + ", " +
                       "stock_price: " + str(stock_price))
        return redirect(url_for('confirmation', err=errors.UNEXP))

    logger.info("User with username " + str(username) + " is attempting to sell stock with symbol " + str(symbol) +
                " at a price of " + str(stock_price))

    stocks_map = cache.json
    symbol_map = stocks_map.get(symbol)
    if symbol_map is None:
        logger.warning("User tried to sell stock with symbol " + str(symbol) + " but is not in the stocks map")
        return redirect(url_for('confirmation', err=errors.SDNE))
    server_stock_price = float(symbol_map.get("price"))

    if stock_price < 0:
        logger.warning("User with username " + str(username) +
                       " tried to sell stock for a negative price: " + str(stock_price))
        return redirect(url_for('confirmation', err=errors.UNEXP))

    if quantity <= 0:
        logger.warning("User with username " + str(username) +
                       " tried to sell a negative amount of stock: " + str(quantity))
        return redirect(url_for('confirmation', err=errors.SLESS))

    if stock_price != server_stock_price:
        logger.warning("User tried to sell the stock at price " + str(stock_price) +
                       " but the server stock price was " + str(server_stock_price))
        return redirect(url_for('confirmation', err=errors.PRICH))

    logger.info("User with username " + str(username) + " passed all validations for selling " + str(quantity) +
                " stocks with symbol " + str(symbol) + " at a stock price of " + str(stock_price))
    # sell the stock
    rtn = stock_user_datastore.sell_stocks_from_user(username, symbol, quantity, cache)
    if rtn.get("error"):
        return redirect(url_for('confirmation', err=rtn.get("data")))
    else:
        return redirect(url_for('confirmation'))


# for testing only, TODO: remove this API and get the user data a different way
@app.route("/getUserInfo", methods=['GET'])
@login_required
def get_user_info():
    user_dict = get_user_dict()
    logger.info("Returning user information for " + str(current_user.username))
    logger.info("user_dict: " + str(user_dict))
    return json.dumps(user_dict, sort_keys=True)


def get_user_dict():
    return {'cash': str(current_user.cash), 'stocks_owned': current_user.stocks_owned}


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """
    This method is used to send error messages to the client.
    Whenever an InvalidUsage is raised, this method will be executed.
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def do_every(interval, worker_func, iterations=0):
    """
    Runs a function every interval number of seconds

    :param interval: How often the function should run, in number of seconds
    :param worker_func: The function to run
    :param iterations: Number of iterations to do before stopping, defaults to infinite
    """
    if iterations != 1:
        t = threading.Timer(
            interval,
            do_every, [interval, worker_func, 0 if iterations == 0 else iterations-1]
        )
        t.setDaemon(True)
        t.start()

    worker_func()


def init_cache(cache_path=None):
    global cache
    logger.info("initializing cache")
    cache = Cache(cache_path)
    do_every(15 * 60, cache.update)  # update the cache every 15 minutes
            
if __name__ == "__main__":
    app.debug = False
    toolbar = DebugToolbarExtension(app)

    init_cache()

    # Heroku will define the PORT environment variable, so use it if it is defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))

    # Bind to PORT if defined, otherwise default to 5000.
    # Heroku will define the PORT environment variable, so use it if it is defined
    port = int(os.environ.get('PORT', 5000))

    logger.info("Starting server")
    # run_simple('localhost', port, app, ssl_context=('./ssl_key.crt', './ssl_key.key'))  # use HTTPS in devo

    # host='0.0.0.0' tells your operating system to listen on all public IPs.
    app.run(host='0.0.0.0', port=port)
    # app.run()
