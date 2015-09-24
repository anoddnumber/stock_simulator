from pymongo import MongoClient
from user import User
from invalid_usage import InvalidUsage

class DbAccess:
    def __init__(self, dbname):
        self.dbname = dbname
        self.client = MongoClient()
        self.db = self.client[dbname]

class UsersDbAccess:
    def __init__(self, db_access):
        self.db_access = db_access
        self.db = self.db_access.db

    def createUser(self, user):
        userInDB = self.getUserByUsername(user.username)
        if userInDB is not None:
            print "User already exists. Choose another username."
            raise InvalidUsage('Username already taken.', status_code=400)
        else:
            self.db.users.insert_one(user.getDict())
        return "Successful"

    def getUserByUsername(self, username):
        userDict = self.db.users.find_one({"username": username})
        if userDict is not None:
            return User(userDict)
        print 'No user found with username ' + username
        return None









