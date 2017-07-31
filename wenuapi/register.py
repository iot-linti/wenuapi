from functools import wraps
import json
import base64
from models.user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils import PasswordType
from flask import request, jsonify, redirect, url_for,abort



def log_user(app):

    @app.route('/login', methods=['GET'])
    def log():

        auth = request.authorization
        username = auth.username
        password = auth.password

        if(not username or not password):
            abort(401, description='Please provide an username and/or password.')
        else:
            user = User.login(username,password)
            if user:
                return json.dumps({'token': user.token})

            abort(401, description='Wrong username and/or password.')

    @app.route('/refreshtoken', methods=['GET'])
    def token():

        method = request.method
        resource = request.path
        auth = request.authorization
        token = auth.username

        if(not token):
            abort(401, description='Please provide a token.')
        else:
            user = User.reset_token(token,resource,method)
            if user:
                return json.dumps({'token': user.token})

            abort(401,'Wrong token')

