from flask_mongoengine import Document
from mongoengine import StringField, BooleanField, DateTimeField, DecimalField, DictField, ListField, ReferenceField
from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash
from decimal import Decimal

class Role(Document, RoleMixin):
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)

class User2(Document, UserMixin):
    username = StringField(max_length=255)
    email = StringField(max_length=255)
    password = StringField(max_length=255)
    active = BooleanField(default=True)
    confirmed_at = DateTimeField()
    roles = ListField(ReferenceField(Role), default=[])
    cash = DecimalField(max_length=255, default=50000, precision=2)
    stocks_owned = DictField(default={})

    # def __init__(self, load_from_db = False, **kwargs):
    #     super(User2, self).__init__()
    #
    #     if load_from_db:
    #         self._pw_hash = kwargs.get('password')
    #         self._id = kwargs.get('_id')
    #     else:
    #         self._pw_hash = generate_password_hash(kwargs.get('password'))
    #
    #     self._username = kwargs.get('username')
    #     self.email = kwargs.get('email')
    #     self.password = self._pw_hash
    #     self.confirmed_at = kwargs.get('confirmed_at')
    #     self.cash = kwargs.get('cash')
    #     self.stocks_owned = kwargs.get('stocks_owned')
    #
    def __str__(self):
        # user_dictionary = self.get_dict()
        # user_dictionary.pop("password", None)
        user_dictionary = {
            'username' : self.username,
            'email' : self.email,
            'cash' : self.cash,
            'stocks_owned' : self.stocks_owned
        }
        return str(user_dictionary)

    def check_password(self, password):
        return password == self.password #TODO hash + salt password and check hashed password here
    #
    # # @property
    # # def id(self):
    # #     return self._id
    # #
    # @property
    # def username(self):
    #     return self._username
    #
    # @property
    # def password_hash(self):
    #     return self._pw_hash
    # #
    # # def check_password(self, password):
    # #     return check_password_hash(self._pw_hash, password)
    # #
    # # @property
    # # def email(self):
    # #     return self.email
    # #
    # # @property
    # # def cash(self):
    # #     return self.cash
    # #
    # # @property
    # # def stocks(self):
    # #     return self.stocks
    #
    # def get_rounded_cash(self):
    #     if self.cash is None:
    #         return None
    #     cash = Decimal(self.cash)
    #     cash = '{:.2f}'.format(round(cash, 2))
    #     return cash
    #
    # def get_dict(self):
    #     return {
    #             "username" : self.username,
    #             "password" : self.password_hash,
    #             "email" : self.email,
    #             "cash" : self.cash,
    #             "stocks_owned" : self.stocks
    #             }
