from config import settings
import os
from Utils.decorators import user_auth

from flask_cors import CORS

from flask_restful import Resource, Api

from Systems.Google.views import google_analytics_metrics, search_console_metrics

from Systems.Facebook.views import facebook_insights_metrics

from flask import Flask, request

from user.models import User


from Admin.views import api_bp, admin
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


    app.register_blueprint(api_bp)
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
            connected_systems = request.user.connected_systems
            if connected_systems.get('facebook_insights'):
                connected_systems['facebook_insights']['campaigns'] = list(request.user.metrics.get('facebook_insights',{}).keys())

            if connected_systems.get('google_analytics'):
                try:  # TODO: for now coz it can return a list
                    connected_systems['google_analytics']['filters'] = request.user.metrics.get('google_analytics').get('ga_sessions').keys()
                except:
                    print('nope')


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