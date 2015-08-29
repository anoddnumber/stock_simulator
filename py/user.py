class User():
    def __init__(self, username, password, email):
        self._username = username
        self._password = password
        self._email = email
        
    @property
    def username(self):
        return self._username
    
    @property
    def password(self):
        return self._password
    
    @property
    def email(self):
        return self._email