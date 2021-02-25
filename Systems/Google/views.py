from Utils.decorators import user_auth
import datetime

from flask import request, Blueprint
from flask_restful import Resource, Api

from user.models import User
from Systems.Google import GoogleAuth, GoogleAnalytics
from Systems.Google.SearchConsole import get_site_list, make_sc_request
from Utils import GoogleUtils

google_bp = Blueprint('google_api', __name__)
api = Api(google_bp)


class GoogleAuthLoginApiView(Resource):
    """
    This View is for google login and registration.
    kinda needs a refactoring...
    """

    def options(self):
        return {}, 200

    def post(self):
        code = request.json['code']
        token = request.json['token']
        if (user := User.get(auth_token=token)):

            uri = 'http://localhost:8080'

            access_token, refresh_token = GoogleAuth.code_exchange(code, uri)

            if not refresh_token:
                return {'error': 'No refresh token got. The user needs to revoke access'}, 404

            User.insert_tokens(token, access_token, refresh_token)

            return {'Message': 'Success'}, 200

        return {'Error': 'Wrong auth token'}, 403


class GoogleAuthLoginApiViewMain(Resource):
    """
    This View is for getting assess to google systems.
    kinda needs a refactoring...
    """

    def options(self):
        return {}, 200

    @user_auth
    def post(self):
        code = request.json['code']
        token = request.json['token']

        uri = 'https://melytix.tk'

        access_token, refresh_token = GoogleAuth.code_exchange(code, uri)

        if not refresh_token:
            return {'error': 'No refresh token got. The user needs to revoke access'}, 404

        User.insert_tokens(token, access_token, refresh_token)

        return {'Message': 'Success'}, 200


class GetVerifiedSitesList(Resource):

    def options(self):
        return {}, 200

    @user_auth
    def post(self):
        site_list = get_site_list(request.token)
        return {'site_list': site_list}, 200


class ConnectSearchConsoleAPI(Resource):

    def options(self):
        return {}, 200

    @user_auth
    def post(self):
        if request.user.connected_systems.get('search_console'):
            return {'Error': 'user has already connected to the Search Console'}, 409
        site_url = request.json['site_url']
        User.connect_system(
            request.token, 'search_console',
            {'site_url': site_url})

        start_date = request.user.parse_from_date
        end_date = datetime.datetime.now()
        #TODO: log the time of the api exec
        response = make_sc_request(request.token, site_url, start_date, end_date)

        data = GoogleUtils.prep_dash_metrics(sc_data=response)

        User.insert_data_in_db(request.token, 'search_console', data)
        return {'Message': 'Success'}, 200



def search_console_metrics(request):
    if not request.user.connected_systems.get('search_console'):
        return {'Error': 'Search Console not connected yet'}, 403

    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')


    sc_dict_data = request.user.metrics.get('search_console')
    metric_name = request.json.get('metric')
    metric = sc_dict_data.get(metric_name)
    dates = sc_dict_data.get('sc_dates')

    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    start_date, end_date = GoogleUtils.find_start_and_end_date(dates, start_date, end_date)

    if metric and dates:
        return {'metric': metric[start_date:end_date], 'dates': dates[start_date:end_date]}, 200


class GetViewIdDropDown(Resource):

    def options(self):
        return {}, 200

    @user_auth
    def post(self):
        select_data = GoogleAnalytics.g_get_select_data(request.token)
        return select_data, 200


class PutViewId(Resource):

    def options(self):
        return {}, 200

    @user_auth
    def post(self):
        viewid = GoogleAnalytics.g_get_viewid(
            request.json['account'],
            request.json['web_property'],
            request.token
        )
        User.connect_system(
            request.token, 'google_analytics',
            {'view_id': viewid,
                'account': request.json['account'],
                'account_name': request.json['account_name'],
                'web_property': request.json['web_property'],
                'web_property_name': request.json['web_property_name']})

        return {'Message': 'Success'}, 200


def google_analytics_metrics(request):
    if not request.user.tokens.get('g_access_token'):
        return {'Error': 'user did not gave access to google yet'}, 404

    metric = request.json['metric']
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')

    # filter = request.json['filter']
    if request.user.metrics.get('google_analytics', {}).get('ga_dates'):

        ga_data = request.user.metrics.get('google_analytics')

        metrics = ga_data.get(metric)
        # metric = metric.get(filter)
        dates = ga_data.get('ga_dates')
        start_date, end_date = GoogleUtils.find_start_and_end_date(dates, start_date, end_date)
        if metric and dates:
            return {'metric': metrics[start_date:end_date], 'dates': dates[start_date:end_date]}, 200

    return {'message': f'the metric "{metric}" was not found'}, 404


class FirstRequestGoogleAnalyticsMetrics(Resource):

    def options(self):
        return {}, 200

    @user_auth
    def post(self):
        """
        This view is responsible for connecting Google Analytics to user
        """
        if not request.user.tokens.get('g_access_token'):
            return {'Error': 'user did not gave access to google yet'}, 404

        if request.user.connected_systems.get('google_analytics'):
            return {'Error': 'user has already connected to the GA'}, 409

        start_date = request.user.parse_from_date
        end_date = datetime.datetime.now().date().isoformat()
        #TODO: log the time of the api exec

        token = request.token

        viewid = GoogleAnalytics.g_get_viewid(
            request.json['account'],
            request.json['web_property'],
            token)

        if viewid:
            from tasks.tasks import google_analytics_query_all
            google_analytics_query_all.delay(token, viewid, start_date, end_date)
            User.connect_system(
                token, 'google_analytics',
                {'view_id': viewid,
                    'account': request.json['account'],
                    'account_name': request.json['account_name'],
                    'web_property': request.json['web_property'],
                    'web_property_name': request.json['web_property_name']})
            return {'Message': 'success'}, 200
        return {'Message': 'could not fetch viewid'}


#Google login
api.add_resource(GoogleAuthLoginApiView , '/insert-tokens', methods=['POST', 'OPTIONS'])
api.add_resource(GoogleAuthLoginApiViewMain, '/insert-tokens-main', methods=['POST', 'OPTIONS'])

# google analytics
api.add_resource(GetViewIdDropDown, '/get-select-data', methods=['POST', 'OPTIONS'])
api.add_resource(PutViewId, '/insert-viewid', methods=['POST', 'OPTIONS'])
api.add_resource(FirstRequestGoogleAnalyticsMetrics, '/connect-ga', methods=['POST', 'OPTIONS'])

# search console
api.add_resource(GetVerifiedSitesList, '/get-sites-url', methods=['POST', 'OPTIONS'])
api.add_resource(ConnectSearchConsoleAPI, '/connect-sc', methods=['POST', 'OPTIONS'])
