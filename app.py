import os

from flask_cors import CORS

from flask_restful import Resource, Api

from Systems.Google.views import (GetSearchConsoleDataAPI, GetVerifiedSitesList,
GoogleAuthLoginApiView, GoogleAuthLoginApiViewMain, GetViewIdDropDown,
RetrieveGoogleAnalyticsMetrics)

from Alerts.views import (RetriveUserAlerts)

from flask import Flask, request

from tasks import refresh_metrics, generate_alerts

import user as User

app = Flask(__name__)
app.secret_key = b"\x92K\x1a\x0e\x04\xcc\x05\xc8\x1c\xc4\x04\x98\xef'\x8e\x1bC\xd6\x18'}:\xc1\x14"
app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)

cors = CORS(app)

class HelloView(Resource):
    def options(self):
        return {}, 200

    def get(self):
        return {'Hello': 'World'}


class ManualRefreshMetricsAndAlerts(Resource):
    def get(self, password):
        if password == '7887334Mna':
            #do testing
            refresh_metrics()
            # refresh_metrics().delay()
            generate_alerts()
            # generate_alerts.delay()
            return {'message': 'yes'}
        else:
            return {'Forbiden access to resource'}, 403


class RegistrationView(Resource):
    """The registration endpoint.
       Takes credentials and creates a new user.
       Credentials : email, password"""
    def options(self):
        return {},200

    def post(self):
        email = request.json['email']
        password = request.json['password']
        if not User.query(email=email):
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


class CacheDashboardSettings(Resource):
    def options(self):
        return {}, 200

    def post(self):
        try:
            token = request.json['token']

            if User.query(auth_token=token):
                User.insert_dash_settings(token, request.json['settings'])
                return {'Message': 'Success'}, 200

            return {'Error': 'Wrong auth token'}, 403

        except KeyError:
            return {'Error': 'no credentials provided'}, 403


class GetCachedDashboardSettings(Resource):
    def options(self):
        return {}, 200

    def post(self):
        try:
            token = request.json['token']

            if (user := User.query(auth_token=token)):

                if (settings := user.get('DashSettings')):
                    return {'settings': settings}, 200
                else:
                    return {'Error': 'user has no Dash settings inserted'}, 404

            return {'Error': 'Wrong auth token'}, 403

        except KeyError:
            return {'Error': 'no credentials provided'}, 403



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

#alerts and tips
api.add_resource(RetriveUserAlerts, '/get-alerts', methods=['POST', 'OPTIONS'])

#testing
api.add_resource(ManualRefreshMetricsAndAlerts, '/refresh/<string:password>', methods=['POST', 'GET'])

#DashSettings post and get
api.add_resource(GetCachedDashboardSettings, '/get-dash-settings', methods=['OPTIONS', 'POST'])
api.add_resource(CacheDashboardSettings, '/put-dash-settings', methods=['OPTIONS', 'POST'])
