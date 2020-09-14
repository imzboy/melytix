from flask import Flask, request

from flask_restful import Resource, Api

from flask_cors import CORS

import user as User

from Systems.Google import GoogleAuth, GoogleAnalytics
from Systems.Google.SearchConsole import get_site_list, make_sc_request
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


class GoogleAuthLoginApiView(Resource):
    """This View is for google login"""
    def options(self):
        return {},200

    def post(self):
        code = request.json['code']

        uri = 'http://localhost:8080'

        access_token, refresh_token = GoogleAuth.code_exchange(code, uri)

        if refresh_token == 403:
            return access_token, refresh_token  # error mesage and error code

        email, picture = GoogleAuth.get_google_user_data(access_token)

        if picture == 403:
            return email, picture  # error mesage and error code

        User.register_from_google(email, picture)

        token = User.get_or_create_token(email)

        User.insert_tokens(token, access_token, refresh_token)

        return {'email': email, 'picture': picture, 'auth_token': token}


class GoogleAuthLoginApiViewMain(Resource):
    """This View is for google login"""
    def options(self):
        return {},200

    def post(self):
        code = request.json['code']

        uri = 'https://kraftpy.github.io/MelytixView'

        access_token, refresh_token = GoogleAuth.code_exchange(code, uri)

        if refresh_token == 403:
            return access_token, refresh_token  # error mesage and error code

        email, picture = GoogleAuth.get_google_user_data(access_token)

        if picture == 403:
            return email, picture  # error mesage and error code

        User.register_from_google(email, picture)

        token = User.get_or_create_token(email)

        User.insert_tokens(token, access_token, refresh_token)

        return {'email': email, 'picture': picture, 'auth_token': token}


class GetVerifiedSitesList(Resource):

    def options(self):
        return {},200

    def post(self):
        try:
            token = request.json['token']

            if User.verify_token(token):
                site_list = get_site_list(token)
                return {'site_list': site_list}, 200

            return {'Error': 'Wrong auth token'}, 403

        except KeyError:
            return {'Error': 'no credentials provided'}, 403


class GetSearchConsoleDataAPI(Resource):

    def options(self):
        return {},200

    def post(self):
        try:
            token = request.json['token']
            if User.verify_token(token):

                site_url = request.json['site_url']
                User.insert_site_for_sc(token, site_url)

                response = make_sc_request(token, site_url, request.json['start_date'], request.json['end_date'])

                data = GoogleUtils.prep_dash_metrics(sc_data=response)

                return {'metric': data[request.json['metric']], 'dates': data['sc_dates']}, 200
            return {'Error': 'Wrong auth token'}, 403
        except KeyError:
            return {'Error': 'no credentials provided'}, 403


""" to be able to query all 3 systems and give all metrics to a dashboard need TODO:

    ~Youtube
        1. Utils yt api respose prep_dash_metrics
        Optional - complete YoutubeAnalytics.py"""

class GetViewIdDropDown(Resource):

    def options(self):
        return {},200

    def post(self):
        try:
            token = request.json['token']
            if User.verify_token(token):
                select_data = GoogleAnalytics.g_get_select_data(token)
                return select_data, 200
            return {'Error': 'Wrong auth token'}, 403
        except KeyError:
            return {'Error': 'no credentials provided'}, 403


class PutViewId(Resource):

    def options(self):
        return {},200

    def post(self):
        try:
            token = request.json['token']
            if User.verify_token(token):
                viewid = GoogleAnalytics.g_get_viewid(
                    request.json['account'],
                    request.json['web_property'],
                    token
                )
                User.insert_viewid(token, viewid)
                return {'Message': 'Success'}, 200
            return {'Error': 'Wrong auth token'}, 403
        except KeyError:
            return {'Error': 'no credentials provided'}, 403


class RetrieveGoogleAnalyticsMetrics(Resource):
    def options(self):
        return {},200

    def post(self):
        """This view inserts view id in db and makes a ga query"""
        if User.verify_token(request.json['token']):

            start_date, end_date = request.json['start_date'], request.json['end_date']

            token = request.json['token']

            viewid = GoogleAnalytics.g_get_viewid(
                request.json['account'],
                request.json['web_property'],
                token
            )
            User.insert_viewid(token, viewid)

            metric = request.json['metric']

            if viewid:
                ga_data = GoogleAnalytics.google_analytics_query(token, viewid, start_date, end_date)

                dash_data = GoogleUtils.prep_dash_metrics(ga_data=ga_data)

                GoogleAnalytics.insert_ga_data_in_db(token, dash_data)

                return {'metric':dash_data[metric], 'dates': dash_data['ga_dates']}, 200
            else:
                return {'error': 'could not fetch view id from google'}, 404

        return {'Error': 'Wrong auth token'}, 403

# URLs declaring --------------------------------

# simple test
api.add_resource(HelloView, '/', methods=['GET', 'OPTIONS'])

#Login end points
api.add_resource(RegistrationView, '/registration', methods=['POST', 'OPTIONS'])
api.add_resource(LoginView, '/login', methods=['POST', 'OPTIONS'])

#Google login
api.add_resource(GoogleAuthLoginApiView , '/insert-tokens', methods=['POST', 'OPTIONS'])
api.add_resource(GoogleAuthLoginApiViewMain, '/insert-tokens-main', methods=['POST', 'OPTIONS'])

# google analytics
api.add_resource(GetViewIdDropDown, '/get-select-data', methods=['POST', 'OPTIONS'])
api.add_resource(RetrieveGoogleAnalyticsMetrics, '/get-ga-data', methods=['POST', 'OPTIONS'])

# search console
api.add_resource(GetVerifiedSitesList, '/get-sites-url', methods=['POST', 'OPTIONS'])
api.add_resource(GetSearchConsoleDataAPI, '/get-sc-data', methods=['POST', 'OPTIONS'])
