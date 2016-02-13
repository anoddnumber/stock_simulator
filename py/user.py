from decimal import Decimal
from werkzeug.security import generate_password_hash, check_password_hash

class User():
    def __init__(self, user_dict, load_from_db = False):
        self._username = user_dict.get('username')
        if load_from_db:
            self._pw_hash = user_dict.get('password')
        else:
            self._pw_hash = generate_password_hash(user_dict.get('password'))
        self._email = user_dict.get('email')
        self._cash = user_dict.get('cash')
        self._stocks = user_dict.get('stocks_owned')

    @property
    def username(self):
        return self._username

    @property
    def password_hash(self):
        return self._pw_hash

    def check_password(self, password):
        return check_password_hash(self._pw_hash, password)
    
    @property
    def email(self):
        return self._email
    
    @property
    def cash(self):
        return self._cash
    
    @property
    def stocks(self):
        return self._stocks
    
    def getRoundedCash(self):
        if self.cash is None:
            return None
        cash = Decimal(self.cash)
        cash = '{:.2f}'.format(round(cash, 2))
        return cash
    
    def getDict(self):
        return {
                "username" : self.username,
                "password" : self.password_hash,
                "email" : self.email,
                "cash" : self.cash,
                "stocks" : self.stocks
                }
