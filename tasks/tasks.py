from requests.api import request
import json
import os
from Systems.Google.views import search_console_metrics
from Systems.Google.SearchConsole import make_sc_request
import celery
from Utils import GoogleUtils
from analytics.base import MetricAnalyzer, MetricNotFoundException
from Systems.SiteParser.parser import MainSiteParser, SiteUrls
from Utils.utils import inheritors
import datetime
from bson import ObjectId

from analytics.google_analytics import *
from analytics.search_console import *
from analytics.face_book_insings import *

from Systems.Facebook.FacebookAdsManager import facebook_insights_query
from Systems.Google.GoogleAnalytics import generate_report_body
from Systems.Google.GoogleAuth import auth_credentials
from Systems.GoogleAds.GoogleAds import google_ads_query_metrics
from Utils.GoogleUtils import GoogleReportsParser, GoogleTotalsReportsParser, fill_all_with_zeros
from Utils.FacebookUtils import create_list_of_dates
import tasks
from user.models import User
from googleapiclient.discovery import build
from tasks import celery



@celery.task
def refresh_metrics():
    """
    Makes list of users from DB and calls method for refreshing metrics
    for 10 users by one task
    """
    if (mongo_users := User.filter(metrics={'$exists': True})):
    # if (mongo_users := [User.get(email='info@kith2kin.de')]):
        users = []  # convert pymongo cursor obj to list
        for mongo_user in mongo_users:
            user = {'email': mongo_user.email,
                    'token': mongo_user.auth_token}
            if mongo_user.connected_systems.get('google_analytics'):  #TODO: add more systems
                user['view_id'] = mongo_user.connected_systems['google_analytics']['view_id']
            if mongo_user.connected_systems.get('search_console'):
                user['site_url'] = mongo_user.connected_systems['search_console']['site_url']

            users.append(user)

        # refresh 10 users by one task for more threaded performace
        step = 10
        for id in range(0, len(users), step):
            # refresh_metric((users[id: id + step]))
            refresh_metric.delay((users[id: id + step]))


@celery.task
def refresh_metric(users: list):
    """
    For each user from the list, it makes a request to Google Analytics
    to get updated metrics for today, and updates these metrics in the DB
            Parameters:
                users (list): list of users to update metrics
    """
    # TODO: in future make this function refresh all system metrics that user connects
    for user in users:
        token = user['token']
        view_id = user.get('view_id')
        site_url = user.get('site_url')

        if view_id:
            google_analytics_query_all.delay(token, view_id, 'today', 'today')

        if site_url:
            date = (datetime.datetime.now() - datetime.timedelta(days=3)).date().isoformat()  # SC doesn't return metrics for 3 last days
            response = make_sc_request(token, site_url, date, date)
            data = GoogleUtils.prep_dash_metrics(sc_data=response)

            user_obj = User.get(email=user.get('email'))

            date = data.pop('sc_dates')
            user_obj.metrics.daily_update(data, date, 'search_console')


@celery.task
def generate_tip_or_alert(users: list):
    analytics = MetricAnalyzer.__subclasses__()
    for user in users:
        for analytics_class in analytics:
            try:
                metrics = User.get(email=user.get('email')).metrics
                analytics_class(metrics).__analyze(user.get('_id'))
            except MetricNotFoundException:
                continue


@celery.task
def generate_tips_and_alerts():
    """
    For each user form DB calls methods of generating tips and alerts
    """
    # users = User.filter_only(connected_systems={'$exists': True}, fields={'_id':True, 'auth_token':True})
    # users = [User.get_only(email='art-holst@gmail.com', fields={'_id':True, 'auth_token':True})]
    users = [User.get_only(email='info@kith2kin.de', fields={'_id':True, 'auth_token':True}),
             User.get_only(email='art-holst@gmail.com', fields={'_id':True, 'auth_token':True})]
    for user in users:
        user['_id'] = str(user.get('_id'))

    step = 10
    for i in range(0, len(users), step):
        generate_tip_or_alert.delay(users[i:i+step])


@celery.task
def google_analytics_query_all(token, view_id, start_date, end_date):
    # Max of 10 metrics and 7 dimesions in one report body
    dimensions = ['ga:browser', 'ga:operatingSystem',
                  'ga:mobileDeviceBranding', 'ga:mobileInputSelector', 'ga:mobileDeviceModel',
                  'ga:mobileDeviceInfo', 'ga:deviceCategory', 'ga:browserSize', 'ga:country',
                  'ga:region', 'ga:language', 'ga:userAgeBracket', 'ga:userGender',
                  'ga:interestOtherCategory', 'ga:city']
    dates = create_list_of_dates(start_date, end_date)

    metrics = ['ga:sessions', 'ga:users', 'ga:pageviews',
                     'ga:pageviewsPerSession', 'ga:avgSessionDuration', 'ga:bounces',
                     'ga:percentNewSessions', 'ga:pageviews', 'ga:timeOnPage', 'ga:pageLoadTime',
                     'ga:avgPageLoadTime', 'ga:transactionsPerSession', 'ga:transactionRevenue']

    totals_report = generate_report_body(
    view_id=view_id,
    start_date=start_date,
    end_date=end_date,
    metrics=metrics,
    dimensions=['ga:date'])

    google_analytics_query_totals.delay(totals_report, start_date, end_date, token)


    result = {
        **{k.replace(':', '_'):{} for k in metrics}
    }
    for dimension in dimensions:

        report = generate_report_body(
            view_id=view_id,
            start_date=start_date,
            end_date=end_date,

            metrics=metrics,

            dimensions=['ga:date', dimension])
        res = google_analytics_query(report, start_date, end_date, token)
        res.pop('ga_dates')
        for metric_name, value in res.items():
            result[metric_name].update(**value)

    user = User.get(token=token)
    if len(dates) > 1:
        user.metrics.initial_insert(result, dates, 'google_analytics', table_type='filtered')
    else:
        user.metrics.daily_update(result)

def google_analytics_query(report: list, start_date, end_date, token):
    # Google Analytics v4 api setup to make a request to google analytics
    api_client = build(serviceName='analyticsreporting', version='v4', http=auth_credentials(token), cache_discovery=False)
    response = api_client.reports().batchGet(
        body={
            'reportRequests': report
        }).execute()

    dates = create_list_of_dates(start_date, end_date)

    if response.get('reports')[0].get('data').get('rows'):
        return  GoogleUtils.GoogleReportsParser(response, dates).parse()

    return GoogleUtils.fill_all_with_zeros(response, dates)


@celery.task
def google_analytics_query_totals(report, start_date, end_date, token):
    api_client = build(serviceName='analyticsreporting', version='v4', http=auth_credentials(token), cache_discovery=False)
    response = api_client.reports().batchGet(
        body={
            'reportRequests': report
        }).execute()

    user = User.get(token=token)
    if response.get('reports')[0].get('data').get('rows'):
        parsed_response = GoogleUtils.GoogleTotalsReportsParser(response).parse()
        dates = parsed_response.pop('ga_dates')
        user.metrics.initial_insert(parsed_response, dates, 'google_analytics', table_type='totals')

    else:
        l = len(create_list_of_dates(start_date, end_date))
        metrics = ['ga:sessions', 'ga:users', 'ga:pageviews',
                     'ga:pageviewsPerSession', 'ga:avgSessionDuration', 'ga:bounces',
                     'ga:percentNewSessions', 'ga:pageviews', 'ga:timeOnPage', 'ga:pageLoadTime',
                     'ga:avgPageLoadTime', 'ga:transactionsPerSession', 'ga:transactionRevenue']
        parsed_response = {k: [0] * l for k in metrics}
        user.metrics.initial_insert(parsed_response, l, 'google_analytics', table_type='totals')


@celery.task
def check_accounts_for_delete():
    if mongo_users := User.filter_only(delete_date={'$exists': True}, fields={'_id':False, 'delete_date':True, 'email': True}):
        for mongo_user in mongo_users:
            delete_date = mongo_user.get('delete_date')
            today = datetime.datetime.today().date().isoformat()
            if delete_date == today:
                mongo_user.delete(email=mongo_user.get('email'))


@celery.task
def parse_main_site(user_id: str, url: str):

    result = MainSiteParser(url).parse()

    user = User.get(_id=ObjectId(user_id))
    db = user.metrics.db('site_parser')
    db.insert_one({
        'user_id': ObjectId(user_id),
        'date': datetime.datetime.today()
        **result
    })

    for site in result.get('meta_links'):
        parse_sub_site.delay(user_id, site)


@celery.task
def parse_sub_site(user_id: str, site: str):
    result = SiteUrls(site).parse()

    user = User.get(_id=ObjectId(user_id))
    db = user.metrics.db('site_parser')
    domain = result.pop('domain')

    db.update_one(
            {'user_id': ObjectId(user_id)},
            {'$set': {
                f'sub_sites.{domain}': result
            }}
        )

