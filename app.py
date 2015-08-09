from py.yahoo_stock_api import yahoo_stock_api
from flask import Flask, send_from_directory
app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    print 'root executed'
    #return send_from_directory('.','index.html')
    return app.send_static_file('index.html')
    #return 'hi';
    
@app.route("/info")
def getStockInfo():
    api = yahoo_stock_api(['AAPL', 'GOOG', 'AMZN'], 'nab')
    return api.submitRequest()
            
if __name__ == "__main__":
    app.debug = True
    app.run()
