from flask_mongoengine import Document
from mongoengine import StringField, BooleanField, DateTimeField, DecimalField, DictField, ListField, ReferenceField
from flask_security import UserMixin, RoleMixin
from flask_security.utils import verify_password


class Role(Document, RoleMixin):
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)


class User(Document, UserMixin):
    username = StringField(max_length=255)
    email = StringField(max_length=255)
    password = StringField(max_length=255)
    active = BooleanField(default=True)
    confirmed_at = DateTimeField()
    roles = ListField(ReferenceField(Role), default=[])
    cash = DecimalField(max_length=255, default=50000, precision=2)
    stocks_owned = DictField(default={})

    def __str__(self):
        # user_dictionary = self.get_dict()
        # user_dictionary.pop("password", None)
        user_dictionary = {
            'username': self.username,
            'email': self.email,
            'cash': self.cash,
            'stocks_owned': self.stocks_owned
        }
        return str(user_dictionary)

    def check_password(self, password):
        return verify_password(password, self.password)
