
import datetime
from flask_restful import Resource, Api

from flask import Flask, request

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

            uri = 'https://kraftpy.github.io'

            access_token, refresh_token = GoogleAuth.code_exchange(code, uri)

            User.insert_tokens(token, access_token, refresh_token)

            return {'Message': 'Success'}, 200

        return {'Error': 'Wrong auth token'}, 403

class GetVerifiedSitesList(Resource):

    def options(self):
        return {},200

    def post(self):
        try:
            token = request.json['token']

            if User.query(auth_token=token):
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
            if User.query(auth_token=token):

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
                User.insert_viewid(token, viewid)
                return {'Message': 'Success'}, 200
            return {'Error': 'Wrong auth token'}, 403
        except KeyError:
            return {'Error': 'no credentials provided'}, 403


class RetrieveGoogleAnalyticsMetrics(Resource):

    def options(self):
        return {},200

    def post(self):
        """This view inserts view id in db and makes a ga query for past 3 weeks"""
        if (user := User.query(auth_token=request.json['token'])):

            metric = request.json['metric']

            if (view_id := user.get('G_Analytics').get('viewid')):

                ga_data = user.get('G_Analytics').get('ga_data')

                return {'metric': ga_data[metric], 'dates': ga_data['ga_dates']}, 200

            else:
                # start_date, end_date = request.json['start_date'], request.json['end_date']
                thee_weeks_ago = (datetime.datetime.now() - datetime.timedelta(weeks=3)).strftime('%Y-%m-%d')

                start_date, end_date = thee_weeks_ago, 'today'

                token = request.json['token']

                viewid = GoogleAnalytics.g_get_viewid(
                    request.json['account'],
                    request.json['web_property'],
                    token
                )

                User.insert_viewid(token, viewid)

                if viewid:
                    ga_data = GoogleAnalytics.google_analytics_query(token, viewid, start_date, end_date)

                    dash_data = GoogleUtils.prep_dash_metrics(ga_data=ga_data)

                    GoogleAnalytics.insert_ga_data_in_db(token, dash_data)

                    return {'metric':dash_data[metric], 'dates': dash_data['ga_dates']}, 200
                else:
                    return {'error': 'could not fetch view id from google'}, 404

        return {'Error': 'Wrong auth token'}, 403
