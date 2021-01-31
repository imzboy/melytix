
from Utils.GoogleUtils import find_start_and_end_date
import datetime
from flask_restful import Resource

from flask import request

import user as User

from Systems.Google import GoogleAuth, GoogleAnalytics
from Systems.Google.SearchConsole import get_site_list, make_sc_request
from Utils import GoogleUtils


class GoogleAuthLoginApiView(Resource):
    """
    This View is for google login and registration.
    kinda needs a refactoring...
    """
    def options(self):
        return {},200

    def post(self):
        code = request.json['code']
        token = request.json['token']
        if (user := User.query(auth_token=token)):


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
        return {},200

    def post(self):
        code = request.json['code']
        token = request.json['token']
        if (user := User.query(auth_token=token)):

            uri = 'https://melytix.tk'

            access_token, refresh_token = GoogleAuth.code_exchange(code, uri)

            if not refresh_token:
                return {'error': 'No refresh token got. The user needs to revoke access'}, 404

            User.insert_tokens(token, access_token, refresh_token)

            return {'Message': 'Success'}, 200

        return {'Error': 'Wrong auth token'}, 403


class GetVerifiedSitesList(Resource):

    def options(self):
        return {},200

    def post(self):

        if (token := request.json.get('token')):

            if User.query(auth_token=token):
                site_list = get_site_list(token)
                return {'site_list': site_list}, 200

            return {'Error': 'Wrong auth token'}, 403

        return {'Error': 'no credentials provided'}, 403


class ConnectSearchConsoleAPI(Resource):

    def options(self):
        return {}, 200

    def post(self):
        if (token := request.json['token']):
            if(user := User.query(auth_token=token)):
                if user.get('connected_systems', {}).get('search_console'):
                    return {'Error': 'user has already connected to the Search Console'}, 409
                site_url = request.json['site_url']
                User.connect_system(
                    token, 'search_console',
                    {'site_url': site_url})

                three_weeks_ago = (datetime.datetime.now() - datetime.timedelta(weeks=3))
                today = datetime.datetime.now()
                response = make_sc_request(token, site_url, three_weeks_ago, today)

                data = GoogleUtils.prep_dash_metrics(sc_data=response)

                User.insert_data_in_db(token, 'search_console', data)
                return {'Message': 'Success'}, 200

            return {'Error': 'Wrong auth token'}, 403

        return {'Error': 'no credentials provided'}, 403


class GetSearchConsoleDataAPI(Resource):

    def options(self):
        return {},200

    def post(self):
        if (token := request.json['token']):
            if(user := User.query(auth_token=token)):

                if not user.get('connected_systems', {}).get('search_console'):
                    return {'Error': 'Search Console not connected yet'}, 403

                sc_dict_data = user.get('metrics').get('search_console')
                result = {}
                for metric_name, data_list in sc_dict_data:
                    result.update({metric_name: data_list[-7:]})

                return result, 200

            return {'Error': 'Wrong auth token'}, 403

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
            if User.query(auth_token=token):
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
            if User.query(auth_token=token):
                viewid = GoogleAnalytics.g_get_viewid(
                    request.json['account'],
                    request.json['web_property'],
                    token
                )
                User.connect_system(
                    token, 'google_analytics',
                    {'view_id': viewid,
                     'account': request.json['account'],
                     'account_name': request.json['account_name'],
                     'web_property': request.json['web_property'],
                     'web_property_name': request.json['web_property_name']})

                return {'Message': 'Success'}, 200
            return {'Error': 'Wrong auth token'}, 403
        except KeyError:
            return {'Error': 'no credentials provided'}, 403


class RetrieveGoogleAnalyticsMetrics(Resource):

    def options(self):
        return {},200

    def post(self):

        if (user := User.query(auth_token=request.json['token'])):
            if not user.get('tokens').get('g_access_token'):
                return {'Error': 'user did not gave access to google yet'}, 404

            metric = request.json['metric']

            if user.get('metrics', {}).get('google_analytics', {}).get('ga_dates'):

                ga_data = user.get('metrics').get('google_analytics')

                metrics = ga_data.get(metric)
                dates = ga_data.get('ga_dates')
                if metric and dates:
                    metrics = metrics[7:]
                    dates = dates[7:]
                    return {'metric': metrics, 'dates': dates}, 200

                return {'message': f'the metric "{metric}" was not found'}, 404
        return {'Error': 'Wrong auth token'}, 403


class FirstRequestGoogleAnalyticsMetrics(Resource):

    def options(self):
        return {},200

    def post(self):
        """
        This view is responsible for connecting Google Analytics to user
        """
        if (user := User.query(auth_token=request.json['token'])):
            if not user.get('tokens').get('g_access_token'):
                return {'Error': 'user did not gave access to google yet'}, 404

            if user.get('connected_systems', {}).get('google_analytics'):
                return {'Error': 'user has already connected to the GA'}, 409

            thee_weeks_ago = (datetime.datetime.now() - datetime.timedelta(weeks=3)).strftime('%Y-%m-%d')

            start_date, end_date = thee_weeks_ago, 'today'

            token = request.json['token']

            viewid = GoogleAnalytics.g_get_viewid(
                request.json['account'],
                request.json['web_property'],
                token)

            if viewid:
                ga_data = GoogleAnalytics.google_analytics_query(token, viewid, start_date, end_date)
                if ga_data:
                    dash_data = GoogleUtils.GoogleReportsParser(ga_data).parse()
                    User.insert_data_in_db(token, 'google_analytics', dash_data)
                    User.connect_system(
                        token, 'google_analytics',
                        {'view_id': viewid,
                        'account': request.json['account'],
                        'account_name': request.json['account_name'],
                        'web_property': request.json['web_property'],
                        'web_property_name': request.json['web_property_name']})

                    return {'Message': 'success'}, 200
                else:
                    return {'Error': 'Google currently unavailable'}, 403
            else:
                return {'error': 'could not fetch view id from google'}, 404

        return {'Error': 'Wrong auth token'}, 403
