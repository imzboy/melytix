from Admin.views import MainManualAnalyzeView
import os

from flask_cors import CORS

from flask_restful import Resource, Api

from Systems.Google.views import (GetSearchConsoleDataAPI, GetVerifiedSitesList,
GoogleAuthLoginApiView, GoogleAuthLoginApiViewMain, GetViewIdDropDown,
RetrieveGoogleAnalyticsMetrics)

from Alerts.views import RetriveUserAlerts
from Tips.views import RetriveUserTips


from flask import Flask, request, render_template, url_for, redirect

from tasks import refresh_metrics, generate_tips_and_alerts

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
            generate_tips_and_alerts()
            # generate_tips_and_alerts.delay()
            return {'message': 'yes'}
        else:
            return {'Forbiden access to resource'}, 403


@app.route('/admin/', methods=['GET', 'POST'])
def menu():
    return f'<a href="{url_for("reg_a_user")}">register a new user</a><br><a href="{url_for("tips_alert_admin")}">Tips and Alerts Admin</a>'


@app.route('/admin/tips-alerts', methods=['GET', 'POST'])
def tips_alert_admin():
    #TODO: render template by front with js
    return render_template('admin/login/index.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        form = request.form
        login = form.get("login")
        password = form.get("pass")
        if login and password:
            if login == "Melycat" and password == "789456123321654asdasdqqq&":
                return redirect(url_for('menu'))
            else:
                return render_template('admin/login/index.html', url='/admin/login', message='wrong credentials')
    elif request.method == 'GET':
        return render_template('admin/login/index.html', url='/admin/login')
    return '?'


@app.route('/admin/reg-a-user', methods=["GET", "POST"])
def reg_a_user():
    if request.method == 'GET':
        return render_template('admin/login/index.html', url='/admin/reg-a-user')
    elif request.method == 'POST':
        form = request.form
        email = form.get("login")
        password = form.get("pass")
        if email and password:
            if not User.query(email=email):
                User.register(email, password)
                return render_template('admin/login/index.html', message='success', url='/admin/reg-a-user')
            else:
                return render_template('admin/login/index.html', message='user with that email already exists', url='/admin/reg-a-user')
    return '?'

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


class LogOutView(Resource):

    def options(self):
        return {}, 200

    def post(self):
            try:
                token = request.json['token']

                if User.query(auth_token=token):
                    User.find_and_update(
                        {'auth_token': token},
                        {'auth_token': None})
                    return {}, 200

                return {'Error': 'Wrong auth token'}, 403

            except KeyError:
                return {'Error': 'no credentials provided'}, 403


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
# api.add_resource(RegistrationView, '/registration', methods=['POST', 'OPTIONS'])
api.add_resource(LoginView, '/login', methods=['POST', 'OPTIONS'])
api.add_resource(LogOutView, '/logout', methods=['POST', 'OPTIONS'])


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
api.add_resource(RetriveUserTips, '/get-tips', methods=['POST', 'OPTIONS'])

#testing
api.add_resource(ManualRefreshMetricsAndAlerts, '/refresh/<string:password>', methods=['POST', 'GET'])

#DashSettings post and get
api.add_resource(GetCachedDashboardSettings, '/get-dash-settings', methods=['OPTIONS', 'POST'])
api.add_resource(CacheDashboardSettings, '/put-dash-settings', methods=['OPTIONS', 'POST'])

#Admin
api.add_resource(MainManualAnalyzeView, '/admin-api', methods=['OPTIONS', 'POST', 'GET'])