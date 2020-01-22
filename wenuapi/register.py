# coding=utf-8
'''Browseable route to login and fetch an api key from the API'''

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
        '''
        Endpoint fuera de Eve. Se utiliza para loguearse por
        medio de usuario y contraseña. Se actualiza el token y se lo retorna
        '''

        auth = request.authorization
        if auth is not None:
            username = auth.username
            password = auth.password
        else:
            username = password = False

        if(not username or not password):
            abort(401, description='Please provide an username and/or password.')
        else:
            user = User.login(username,password)
            if user:
                return json.dumps({'token': user.token})

            abort(401, description='Wrong username and/or password.')

    @app.route('/refreshtoken', methods=['GET'])
    def token():
        '''
        Se utiliza para renovar el token de un usuario, sin necedidad de
        enviar el usuario y contraseña
        '''

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

