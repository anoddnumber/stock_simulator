from py.yahoo_stock_api import yahoo_stock_api
from flask import Flask, send_from_directory, request
app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')
    
@app.route("/info")
def getStockInfo():
    symbols = request.args.get('symbols')
    if symbols == None:
        return 'No symbols were in the get request'
    symbols = [x.strip() for x in symbols.split(',')]


    '''
    To find out what options the yahoo_stock_api has, view http://www.jarloo.com/yahoo_finance/
    '''
    api = yahoo_stock_api(symbols, 'nabl1')
    return api.submitRequest()


@app.route("/createAccount", methods=['POST'])
def createAccount():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    print username
    print password
    print email
    print "createAccount()"
    return "Created Account!"

            
if __name__ == "__main__":
    app.debug = True
    app.run()
