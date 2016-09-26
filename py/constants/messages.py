def get_sell_success_message(quantity, symbol, price_per_stock):
    return 'You have successfully sold ' + str(int(quantity)) + ' shares of ' + str(symbol) + ' at ' + \
           str(price_per_stock) + ' per stock.'


def get_buy_success_message(quantity, symbol, price_per_stock):
    return 'You have successfully bought ' + str(int(quantity)) + ' shares of ' + str(symbol) + ' at ' + \
           str(price_per_stock) + ' per stock.'




