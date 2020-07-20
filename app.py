from flask import Flask, request

from flask_restful import Resource, Api

from flask_cors import CORS

import user as User

from Systems.Google import GoogleAuth
from Utils import GoogleUtils

app = Flask(__name__)
app.secret_key = b"\x92K\x1a\x0e\x04\xcc\x05\xc8\x1c\xc4\x04\x98\xef'\x8e\x1bC\xd6\x18'}:\xc1\x14"

app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)

cors = CORS(app)

class HelloView(Resource):
    def get(self):
        return {'Message': 'Hello World!'}


class RegistrationView(Resource):
    """The registration endpoint.
       Takes credentials and creates a new user.
       Credentials : email, password"""
    def options(self):
        return {},200


    def post(self):
        email = request.json['email']
        password = request.json['password']
        if not User.get_by_email(email):
            User.register(email, password)
            return {'status': 'success',
                    'email': email}
        else:
            return {'Error': 'User with that email already created'}


class LoginView(Resource):
    def options(self):
        return {},200

    def post(self):
        email = request.json['email']
        password = request.json['password']
        verify = User.verify_password(email, password)
        if verify and verify != 404:
            return {'token': User.get_or_create_token(email)}
        elif verify == 404:
            return {'Error': 'user not found'}, 404
        else:
            return {'Error': 'wrong password'}


class InsertGoogleTokensApiView(Resource):

    def options(self):
        return {},200

    def put(self):
        if User.verify_token(request.json['token']):

            google_tokens = request.json['google_token']
            if User.insert_tokens(request.json['token'], google_tokens[0], google_tokens[1]):
                return {'Status': 'success'}, 200
            else:
                return "User email not available or not verified by Google.", 403

        return {'Error': 'Wrong auth token'}, 403


# URLs declaring
api.add_resource(HelloView, '/', methods=['GET', 'OPTIONS'])
api.add_resource(RegistrationView, '/registration', methods=['POST', 'OPTIONS'])
api.add_resource(LoginView, '/login', methods=['POST', 'OPTIONS'])
api.add_resource(InsertGoogleTokensApiView , '/insert-tokens', methods=['PUT', 'OPTIONS'])
