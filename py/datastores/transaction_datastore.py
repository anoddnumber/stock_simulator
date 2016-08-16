from flask_security.datastore import MongoEngineDatastore
from py.user import Transaction


class MongoEngineTransactionDatastore(MongoEngineDatastore):
    def find_transactions(self, user_id):
        """
        :param user_id: The user's ID (has type ObjectId)
        :return: A list of transaction Objects associated with the user
        """
        from mongoengine import ValidationError
        try:
            return Transaction.objects(user_id=user_id)
        except ValidationError:
            # TODO: is there a way to handle this? look at MongoEngineUserDatastore
            return None

    def create_transaction(self, user_id, properties):
        transaction = Transaction(user_id=user_id, properties=properties)
        return self.put(transaction)
