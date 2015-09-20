from decimal import Decimal

class User():
#     def __init__(self, username, password, email):
#         self._username = username
#         self._password = password
#         self._email = email
        
    def __init__(self, dict):
        self._username = dict.get('username')
        self._password = dict.get('password')
        self._email = dict.get('email')
        self._cash = dict.get('cash')
        
    @property
    def username(self):
        return self._username
    
    @property
    def password(self):
        return self._password
    
    @property
    def email(self):
        return self._email
    
    @property
    def cash(self):
        return self._cash
    
    def getRoundedCash(self):
        cash = Decimal(self._cash)
        cash = '{:.2f}'.format(round(cash, 2))
        return cash
