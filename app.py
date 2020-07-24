from flask import Flask, request

from flask_restful import Resource, Api

from flask_cors import CORS

import user as User

from Systems.Google import GoogleAuth
from Systems.Google.SearchConsole import get_site_list
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

    def post(self):
        if User.verify_token(request.json['token']):

            code = request.json['code']

            access_token, refresh_token = GoogleAuth.code_exchange(request.json['token'], code)

            User.insert_tokens(request.json['token'], access_token, refresh_token)

            return {'Status': 'success'}, 200

        return {'Error': 'Wrong auth token'}, 403


class GetVerifiedSitesList(Resource):

    def options(self):
        return {},200

    def post(self):
        try:
            token = request.json['token']

            if User.verify_token(token):
                scopes = User.get_scopes(token)
                if 'sc' in scopes:
                    site_list = get_site_list(token)
                    return {'site_list': site_list}, 200

            return {'Error': 'Wrong auth token'}, 403

        except KeyError:
            return {'Error': 'no credentials provided'}, 403


""" to be able to query all 3 systems and give all metrics to a dashboard need TODO:
    ~Google Analytics:
        1. make an api for retrieving select_data for viewid
        2. make and api that posts the select_data from user to a viewid function

    ~Search Console:
        1. make an api to register a client site in db
        2. make 1 api to query all servises

    ~Youtube
        1. Utils yt api respose prep_dash_metrics
        Optional - complete YoutubeAnalytics.py"""

class RetrivieveDashboardMetrics(Resource):
    #  too soon
    def options(self):
        return {},200

    def post(self):  # TODO: start date, end date
        if User.verify_token(request.json['token']):
            pass


        return {'Error': 'Wrong auth token'}, 403

# URLs declaring
api.add_resource(HelloView, '/', methods=['GET', 'OPTIONS'])
api.add_resource(RegistrationView, '/registration', methods=['POST', 'OPTIONS'])
api.add_resource(LoginView, '/login', methods=['POST', 'OPTIONS'])
api.add_resource(InsertGoogleTokensApiView , '/insert-tokens', methods=['POST', 'OPTIONS'])
