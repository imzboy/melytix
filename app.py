from Utils.decorators import user_auth
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_cors import CORS
from bson import ObjectId

from flask_restful import Resource, Api

from Admin.views import MainManualAnalyzeView

from Systems.Google.views import (GetSearchConsoleDataAPI, GetVerifiedSitesList,
GoogleAuthLoginApiView, GoogleAuthLoginApiViewMain, GetViewIdDropDown, PutViewId,
RetrieveGoogleAnalyticsMetrics, FirstRequestGoogleAnalyticsMetrics, ConnectSearchConsoleAPI)

from Systems.Facebook.views import (FacebookSetAccount,
FacebookAuthLoginApiView, RetrieveFacebookMetricsFromBD)


from Alerts.views import AlertTipFlipActive, RetriveUserAlerts
from Tips.views import RetriveUserTips

from flask import Flask, request, render_template, url_for, redirect

from tasks import refresh_metrics, generate_tips_and_alerts

from user import User, Admin

app = Flask(__name__)
app.secret_key = b"\x92K\x1a\x0e\x04\xcc\x05\xc8\x1c\xc4\x04\x98\xef'\x8e\x1bC\xd6\x18'}:\xc1\x14"
app.config['CORS_HEADERS'] = 'Content-Type'

login = LoginManager(app)
login.login_view = '/admin/login'

api = Api(app)

cors = CORS(app)


@login.user_loader
def load_user(id):
    return Admin(Admin.get(_id=ObjectId(id)))


class HelloView(Resource):
    def options(self):
        return {}, 200

    def get(self):
        return {'Hello': 'World'}


@app.route('/refresh', methods=['GET'])
@login_required
def refresh():
    refresh_metrics()

    # generate_tips_and_alerts()
    # generate_tips_and_alerts.delay()
    return {'message': 'yes'}


@app.route('/admin/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin_login'))



@app.route('/admin/', methods=['GET', 'POST'])
@login_required
def menu():
    return f'<a href="{url_for("reg_a_user")}">register a new user</a>' \
    f'<br><a href="https://admin.melytix.tk/">Tips and Alerts Admin</a>' \
    f'<br><a href="{url_for("logout")}">logout</a>' \
    f'<br><a href="/refresh">refresh metrics</a>'


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        form = request.form
        login = form.get("login")
        password = form.get("pass")
        if login and password:
            if User.verify_admin_password(login, password):
                login_user(Admin(Admin.get(email=login)))
                return redirect(url_for('menu'))
            else:
                return render_template('admin/login/index.html', url='/admin/login', message='wrong credentials')
    elif request.method == 'GET':
        return render_template('admin/login/index.html', url='/admin/login')
    return '?'


@app.route('/admin/reg-a-user', methods=["GET", "POST"])
@login_required
def reg_a_user():
    if request.method == 'GET':
        return render_template('admin/login/index.html', url='/admin/reg-a-user')
    elif request.method == 'POST':
        form = request.form
        email = form.get("login")
        password = form.get("pass")
        if email and password:
            if not User.get(email=email):
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
        if User.verify_password(email, password):
            return {'token': User.get_or_create_token(email)}
        return {'Error': 'wrong password'}


class LogOutView(Resource):

    def options(self):
        return {}, 200

    @user_auth
    def post(self):
        User.update_one(
            {'auth_token': request.user.token},
            {'auth_token': None})
        return {'Message': 'User logout'}, 200


class CacheDashboardSettings(Resource):
    def options(self):
        return {}, 200

    @user_auth
    def post(self):

        User.insert_dash_settings(request.user.token, request.json.get('settings'))
        return {'Message': 'Success'}, 200


class GetCachedDashboardSettings(Resource):
    def options(self):
        return {}, 200

    @user_auth
    def post(self):
        if (settings := request.user.DashSettings):

            return {'settings': settings}, 200

        return {'Error': 'user has no Dash settings inserted'}, 404


class MainView(Resource):
    def options(self):
        return {}, 200

    @user_auth
    def post(self):
        return_dict = {}
        return_dict.update(request.user.connected_systems)
        return {**return_dict}, 200



class DashboardWidgetView(Resource):

    def options(self):
        return {}, 200

    def post(self):
        pass


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
api.add_resource(PutViewId, '/insert-viewid', methods=['POST', 'OPTIONS'])
api.add_resource(RetrieveGoogleAnalyticsMetrics, '/get-ga-data', methods=['POST', 'OPTIONS'])
api.add_resource(FirstRequestGoogleAnalyticsMetrics, '/connect-ga', methods=['POST', 'OPTIONS'])

# search console
api.add_resource(GetVerifiedSitesList, '/get-sites-url', methods=['POST', 'OPTIONS'])
api.add_resource(ConnectSearchConsoleAPI, '/connect-sc', methods=['POST', 'OPTIONS'])
api.add_resource(GetSearchConsoleDataAPI, '/get-sc-data', methods=['POST', 'OPTIONS'])

# facebook insights
api.add_resource(FacebookSetAccount, '/insert-fi-account', methods=['POST', 'OPTIONS'])
api.add_resource(FacebookAuthLoginApiView, '/insert-fi-token', methods=['POST', 'OPTIONS'])
api.add_resource(RetrieveFacebookMetricsFromBD, '/get-fi-data', methods=['POST', 'OPTIONS'] )

#alerts and tips
api.add_resource(RetriveUserAlerts, '/get-alerts', methods=['POST', 'OPTIONS'])
api.add_resource(RetriveUserTips, '/get-tips', methods=['POST', 'OPTIONS'])
api.add_resource(AlertTipFlipActive, '/flip', methods=['POST', 'OPTIONS'])

#DashSettings post and get
api.add_resource(GetCachedDashboardSettings, '/get-dash-settings', methods=['OPTIONS', 'POST'])
api.add_resource(CacheDashboardSettings, '/put-dash-settings', methods=['OPTIONS', 'POST'])

#DashBoard widget
api.add_resource(DashboardWidgetView, '/get-widget-data', methods=['OPTIONS', 'POST'])

#Main api
api.add_resource(MainView, '/main', methods=['OPTIONS', 'POST'])

#Admin
api.add_resource(MainManualAnalyzeView, '/admin-api', methods=['OPTIONS', 'POST', 'GET'])