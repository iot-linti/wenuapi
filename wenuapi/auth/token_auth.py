from eve.auth import TokenAuth
from ..models.user import User
from flask import current_app as app
from flask import request, Response, abort
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps


import hashlib
import string
import random

from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer
from itsdangerous import SignatureExpired, BadSignature

class TokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        user = User.token_login(token,resource,method,allowed_roles)
        return user

def authenticate():
    print 'fallo'
    """Sends a 401 response that enables basic auth"""
    resp = Response(
        None,
        401,
        {'WWW-Authenticate': 'Basic realm:"%s"' % realm},
    )
    abort(401, description='Please provide proper credentials', response=resp)

def requires_auth(f):
    '''This decorator makes a route to require a loggedin client.
    If the client making the request logged in it returns a response with a
    401 HTTP error'''
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        method = request.method
        resource = request.path
        if not auth or not User.token_login(auth.username,resource,method):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
