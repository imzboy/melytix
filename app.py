from flask_login import LoginManager
from config import settings
import os
import json
from Utils.decorators import user_auth

from flask_cors import CORS

from flask_restful import Resource, Api

from Systems.Google.views import google_analytics_metrics, search_console_metrics

from Systems.Facebook.views import facebook_insights_metrics

from Systems.GoogleAds.views import google_ads_metrics

from Systems.Google.GoogleAuth import CLIENT_ID, code_exchange

from flask import Flask, request, redirect

from user.models import User, Admin
from bson import ObjectId


from Admin.views import admin
from user.views import user_bp
from analytics.views import algorithms_bp
from Systems.Google.views import google_bp
from Systems.Facebook.views import facebook_insg_bp
from Systems.SiteParser.views import parser_bp
from Systems.GoogleAds.views import google_ads_bp

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
    app.register_blueprint(google_ads_bp)


    @app.route('/')
    def hello_world():
        return 'Hello, World!'


    @app.route('/google-redirect')
    def google_redirect():
        code = request.args.get('code')
        token, service = request.args.get('state').split(',')
        print(f'code - {code}')

        uri = 'https://melyback.tk/google_redirect'

        access, refresh = code_exchange(code, uri, token)

        User.insert_tokens(token, access, refresh)

        return redirect(f'https://system.melytix.com/Support/?q={service}')



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
            main_dict = {}
            if request.user.connected_systems:
                main_dict = request.user.connected_systems
                main_dict['g_scopes'] = []


                if main_dict.get('facebook_insights'):
                    metrics_today = request.user.metrics.last_date('facebook_insights')
                    main_dict['facebook_insights']['campaigns'] = list(metrics_today.keys())

                if main_dict.get('google_ads'):
                    metrics_today = request.user.metrics.last_date('google_ads')
                    main_dict['g_scopes'].extend(main_dict.get('google_ads').get('scopes'))
                    main_dict.get('google_ads').pop('scopes')
                    main_dict['google_ads']['campaigns'] = list(metrics_today.keys())

                if main_dict.get('google_analytics'):
                    try:  # TODO: for now coz it can return a list
                        metrics_today = request.user.metrics.last_date('google_analytics', table_type='totals')
                        main_dict['g_scopes'].extend(main_dict.get('google_analytics').get('scopes'))
                        main_dict.get('google_analytics').pop('scopes')
                        main_dict['google_analytics']['metrics'] = list(metrics_today.keys())
                        main_dict['google_analytics']['metrics'].pop('ga_dates')

                        metrics_today = request.user.metrics.last_date('google_analytics', table_type='filtered')
                        main_dict['google_analytics']['filters'] = list(metrics_today.get('ga_sessions').keys())

                        i = main_dict['google_analytics']['filters'].index('dates')
                        main_dict['google_analytics']['filters'].pop(i)
                    except:
                        print('nope')
                if main_dict.get('search_console'):
                    metrics_today = request.user.metrics.last_date('search_console')
                    main_dict['g_scopes'].extend(main_dict.get('search_console').get('scopes'))
                    main_dict.get('search_console').pop('scopes')
                    main_dict['search_console']['metrics'] = list(metrics_today.keys())

                    i = main_dict['search_console']['metrics'].index('dates')
                    main_dict['search_console']['metrics'].pop(i)

            main_dict['language'] = request.user.language
            main_dict['email'] = request.user.email

            return {**main_dict}, 200



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