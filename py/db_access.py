from pymongo import MongoClient
from user import User

class DbAccess:
    def __init__(self, dbname):
        self.dbname = dbname
        self.client = MongoClient()
        self.db = self.client[dbname]

class UsersDbAccess:
    def __init__(self, db_access):
        self.db_access = db_access
        self.db = self.db_access.db

    def saveUser(self, user):
        self.db.users.insert_one({"username" : user.username, "email" : user.email, "password" : user.password})
        return "Successful"

    def getUserByUsername(self, username):
        user = self.db.users.find_one({"username": username})
        if user is not None:
            print user
            return User(user['username'], user['password'], user['email'])
        print 'No user found with username ' + username
        return None









