from flask_login import LoginManager
from config import settings
import os
import json
from Utils.decorators import user_auth

from flask_cors import CORS

from flask_restful import Resource, Api

from Systems.Google.views import google_analytics_metrics, search_console_metrics

from Systems.Facebook.views import facebook_insights_metrics

from flask import Flask, request

from user.models import User, Admin
from bson import ObjectId


from Admin.views import admin
from user.views import user_bp
from analytics.views import algorithms_bp
from Systems.Google.views import google_bp
from Systems.Facebook.views import facebook_insg_bp
from Systems.SiteParser.views import parser_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = b"\x92K\x1a\x0e\x04\xcc\x05\xc8\x1c\xc4\x04\x98\xef'\x8e\x1bC\xd6\x18'}:\xc1\x14"
    APP_ENV = os.environ.get('APP_ENV', 'Dev')
    config = getattr(settings, f'{APP_ENV}Config')
    app.config.update(config.as_dict())

    api = Api(app)

    cors = CORS(app, resources={r"*": {"origins": "*"}})

    login = LoginManager(app)
    login.login_view = '/admin/login'


    @login.user_loader
    def load_user(id):
        return Admin.get(_id=ObjectId(id))


    app.register_blueprint(admin)
    app.register_blueprint(user_bp)
    app.register_blueprint(google_bp)
    app.register_blueprint(facebook_insg_bp)
    app.register_blueprint(algorithms_bp)
    app.register_blueprint(parser_bp)


    @app.route('/')
    def hello_world():
        return 'Hello, World!'

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
            connected_systems = {}
            if request.user.connected_systems:
                connected_systems = request.user.connected_systems
                with open(f'users_metrics/{request.token}/metrics.json', 'r') as f:
                    metrics = json.loads(f.read())
                if connected_systems.get('facebook_insights'):
                    connected_systems['facebook_insights']['campaigns'] = list(metrics.get('facebook_insights',{}).keys())

                if connected_systems.get('google_analytics'):
                    try:  # TODO: for now coz it can return a list
                        connected_systems['google_analytics']['metrics'] = list(metrics.get('google_analytics').keys())
                        ga_dates_i = connected_systems['google_analytics']['metrics'].index('ga_dates')
                        connected_systems['google_analytics']['metrics'].pop(ga_dates_i)

                        connected_systems['google_analytics']['filters'] = list(metrics.get('google_analytics').get('ga_sessions').keys())
                        ga_dates_i = connected_systems['google_analytics']['filters'].index('ga_dates')
                        connected_systems['google_analytics']['filters'].pop(ga_dates_i)
                    except:
                        print('nope')
                if connected_systems.get('search_console'):
                    connected_systems['search_console']['metrics'] = list(metrics.get('search_console').keys())
                    ga_dates_i = connected_systems['search_console']['metrics'].index('sc_dates')
                    connected_systems['search_console']['metrics'].pop(ga_dates_i)


            return {**connected_systems}, 200



    class DashboardWidgetView(Resource):

        def options(self):
            return {}, 200

        @user_auth
        def post(self):
            '''
            uses globals to find a function for getting metrics out of a system
            name a function that retrives metrics from db '{system_name same as in db}_metrics'
            '''
            system = request.json.get('system')
            return globals().get(f'{system}_metrics')(request)


    #DashSettings post and get
    api.add_resource(GetCachedDashboardSettings, '/get-dash-settings', methods=['OPTIONS', 'POST'])
    api.add_resource(CacheDashboardSettings, '/put-dash-settings', methods=['OPTIONS', 'POST'])

    #DashBoard widget
    api.add_resource(DashboardWidgetView, '/get-widget-data', methods=['OPTIONS', 'POST'])

    #Main api
    api.add_resource(MainView, '/main', methods=['OPTIONS', 'POST'])


    return app


# app=create_app()
# app.run(host='0.0.0.0', debug=True)