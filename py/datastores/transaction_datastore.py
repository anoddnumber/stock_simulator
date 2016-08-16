from flask_security.datastore import MongoEngineDatastore
from py.user import Transaction


class MongoEngineTransactionDatastore(MongoEngineDatastore):
    def find_transactions(self, username):
        pass

    def create_transaction(self, user_id, properties):
        transaction = Transaction(user_id=user_id, properties=properties)
        return self.put(transaction)
