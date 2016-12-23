from .models.user import User
from .settings import realm
from eve.auth import BasicAuth
from flask import request, Response, abort
from functools import wraps

class WenuBasicAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        return User.login(username, password)



# The following functions are for custom Flask endpoints. Eve related code
# shouldn't use these functions.

def authenticate():
    """Sends a 401 response that enables basic auth"""
    resp = Response(
        None,
        401,
        {'WWW-Authenticate': 'Basic realm:"%s"' % realm},
    )
    abort(401, description='Please provide proper credentials', response=resp)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not User.login(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

