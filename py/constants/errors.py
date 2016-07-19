UNEXP = 'UNEXP'
SDNE = 'SDNE'
PRICH = 'PRICH'
SLESS = 'SLESS'
BLESS = 'BLESS'
BNEC = 'BNEC'
NESTK = 'NESTK'

ERROR_CODE_MAP = {
    UNEXP: 'An unexpected error has occurred. Please try doing the transaction again.',
    SDNE:  'The stock does not exist in our database.',
    PRICH: 'The stock price has changed, please try the transaction again.',
    SLESS: 'Please specify a quantity of 1 or more shares of stock to sell.',
    BLESS: 'Please specify a quantity of 1 or more shares of stock to buy.',
    BNEC:  'You don\'t have enough cash to buy the stocks. Please try again.',
    NESTK: 'You don\'t own enough shares to sell this stock. Please try again.'
}