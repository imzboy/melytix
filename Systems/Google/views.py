from Utils.decorators import user_auth
import datetime

from flask import request
from flask_restful import Resource

from user import User
from Systems.Google import GoogleAuth, GoogleAnalytics
from Systems.Google.SearchConsole import get_site_list, make_sc_request
from Utils import GoogleUtils
from tasks import google_analytics_query_all


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

        three_weeks_ago = (datetime.datetime.now() - datetime.timedelta(weeks=3))
        today = datetime.datetime.now()
        response = make_sc_request(request.token, site_url, three_weeks_ago, today)

        data = GoogleUtils.prep_dash_metrics(sc_data=response)

        User.insert_data_in_db(request.token, 'search_console', data)
        return {'Message': 'Success'}, 200



class GetSearchConsoleDataAPI(Resource):

    def options(self):
        return {}, 200

    @user_auth
    def post(self):

        if not request.user.connected_systems.get('search_console'):
            return {'Error': 'Search Console not connected yet'}, 403

        sc_dict_data = request.user.metrics.get('search_console')
        result = {}
        for metric_name, data_list in sc_dict_data.items():
            result.update({metric_name: data_list[-7:]})

        return result, 200


""" to be able to query all 3 systems and give all metrics to a dashboard need TODO:

    ~Youtube
        1. Utils yt api respose prep_dash_metrics
        Optional - complete YoutubeAnalytics.py"""


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


class RetrieveGoogleAnalyticsMetrics(Resource):

    def options(self):
        return {}, 200

    def get(self):
        metrics = ['ga:sessions', 'ga:users', 'ga:pageviews',
                   'ga:pageviewsPerSession', 'ga:avgSessionDuration', 'ga:bounces',
                   'ga:percentNewSessions', 'ga:pageviews', 'ga:timeOnPage', 'ga:pageLoadTime',
                   'ga:avgPageLoadTime', 'ga:transactionsPerSession', 'ga:transactionRevenue'],

        filters = ['ga:date', 'ga:browser', 'ga:browserVersion', 'ga:operatingSystem',
                   'ga:browser', 'ga:browserVersion', 'ga:operatingSystemVersion', 'ga:mobileDeviceBranding',
                   'ga:mobileInputSelector', 'ga:mobileDeviceModel', 'ga:mobileDeviceInfo',
                   'ga:deviceCategory', 'ga:browserSize', 'ga:country', 'ga:region', 'ga:city',
                   'ga:language', 'ga:userAgeBracket', 'ga:userGender', 'ga:interestOtherCategory']

        return {"metrics": metrics, "filters": filters}, 200

    @user_auth
    def post(self):

        if not request.user.tokens.get('g_access_token'):
            return {'Error': 'user did not gave access to google yet'}, 404

        metric = request.json['metric']
        # filter = request.json['filter']
        if request.user.metrics.get('google_analytics', {}).get('ga_dates'):

            ga_data = request.user.metrics.get('google_analytics')

            metrics = ga_data.get(metric)
            # metric = metric.get(filter)
            dates = ga_data.get('ga_dates')
            if metric and dates:
                metrics = metrics[7:]
                dates = dates[7:]
                return {'metric': metrics, 'dates': dates}, 200

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

        three_weeks_ago = (datetime.datetime.now() - datetime.timedelta(weeks=3)).date().isoformat()

        start_date, end_date = three_weeks_ago, 'today'

        token = request.json['token']

        viewid = GoogleAnalytics.g_get_viewid(
            request.json['account'],
            request.json['web_property'],
            token)

        if viewid:
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
