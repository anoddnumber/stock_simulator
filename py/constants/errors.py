UNEXPECTED_ERROR = 'An unexpected error has occurred. Please try doing the transaction again.'
STOCK_DOES_NOT_EXIST = 'The stock does not exist in our database.'
PRICE_CHANGED = 'The stock price has changed, please try the transaction again.'

SELL_LESS_THAN_ONE = 'Please specify a quantity of 1 or more shares of stock to sell.'
BUY_LESS_THAN_ONE = 'Please specify a quantity of 1 or more shares of stock to buy.'
BUY_NOT_ENOUGH_CASH = 'You don\'t have enough cash to buy the stocks. Please try again.'


UNEXP = 'UNEXP'
SDNE = 'SDNE'
PRICH = 'PRICH'
SLESS = 'SLESS'
BLESS = 'BLESS'
BNEC = 'BNEC'

ERROR_CODE_MAP = {
    UNEXP: UNEXPECTED_ERROR,
    SDNE: STOCK_DOES_NOT_EXIST,
    PRICH: PRICE_CHANGED,
    SLESS: SELL_LESS_THAN_ONE,
    BLESS: BUY_LESS_THAN_ONE,
    BNEC: BUY_NOT_ENOUGH_CASH
}