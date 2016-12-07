from eve.auth import BasicAuth
from models.user import User

class WenuBasicAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        return User.login(username, password)
