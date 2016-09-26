from flask_security.datastore import MongoEngineDatastore
from py.user import Snapshot


class MongoEngineSnapshotDatastore(MongoEngineDatastore):
    def find_snapshots(self, user_id):
        """
        :param user_id: The user's ID (has type ObjectId)
        :return: A list of Snapshot objects associated with the user
        """
        from mongoengine import ValidationError
        try:
            return Snapshot.objects(user_id=user_id)
        except ValidationError:
            # TODO: is there a way to handle this? look at MongoEngineUserDatastore
            return None

    def create_snapshot(self, user_id, cash, stocks_owned):
        snapshot = Snapshot(user_id=user_id, cash=cash, stocks_owned=stocks_owned)
        return self.put(snapshot)
