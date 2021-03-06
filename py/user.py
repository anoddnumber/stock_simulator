from flask_mongoengine import Document
from mongoengine import StringField, BooleanField, DateTimeField, DecimalField, DictField, ListField, ReferenceField, \
    ObjectIdField
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
    last_transaction = DictField(default={})

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


# Note that the transaction creation date is encoded in the _id field, so we don't have to create another
# field for it here
class Transaction(Document):
    """
    A Transaction is an object that contains information about whether a user bought or sold a stock and how much
    was bought or sold on a particular date.
    """
    user_id = ObjectIdField()  # Reference to the User's _id
    properties = DictField(default={})  # The properties may be different based on the type of transaction


# Note that the creation date is encoded in the _id field, so we don't have to create another
# field for it here
class Snapshot(Document):
    """
    A Snapshot contains how much cash a user has and what stocks a user owns on a particular date.
    """
    user_id = ObjectIdField()  # Reference to the User's _id
    cash = DecimalField(max_length=255, default=50000, precision=2)
    stocks_owned = DictField(default={})
