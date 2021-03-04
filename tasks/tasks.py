import json
import os
from Systems.Google.views import search_console_metrics
from Systems.Google.SearchConsole import make_sc_request
import celery
from Utils import GoogleUtils
from analytics.base import MetricAnalyzer, MetricNotFoundException
from Utils.utils import inheritors
import datetime

from analytics.google_analytics import *
from analytics.search_console import *
from analytics.face_book_insings import *

from Systems.Facebook.FacebookAdsManager import facebook_insights_query
from Systems.Google.GoogleAnalytics import generate_report_body
from Systems.Google.GoogleAuth import auth_credentials
from Utils.GoogleUtils import GoogleReportsParser, GoogleTotalsReportsParser, fill_all_with_zeros
from Utils.FacebookUtils import create_list_of_dates
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
            with open(f'users_metrics/{token}/metrics.json', 'r+') as f:
                all_metrics = json.loads(f.read())
                sc_metrics = all_metrics.pop('search_console')
                for metrics_name, metric_value in sc_metrics.items():
                    metric_value.append(data.get(metrics_name)[0])

                all_metrics['search_console'] = sc_metrics
                f.write(json.dumps(all_metrics))

        # f_metrics = facebook_insights_query(token, today, today)
        # for campaign, metrics in f_metrics.items():
        #     for metric, value in metrics.items():
        #         User.append_list(
        #             {'email': user['email']},
        #             {f'metrics.facebook_insights.{campaign}.{metric}': {'$each': value}}
        #         )


@celery.task
def generate_tip_or_alert(users:list):
    analytics = MetricAnalyzer.__subclasses__()
    for user in users:
        for analytics_class in analytics:
            try:
                with open(f'users_metrics/{user.get("auth_token")}/metrics.json') as f:
                    metrics = json.loads(r.read())
                analytics_class(user.get('metrics')).analyze(user.get('_id'))
            except MetricNotFoundException:
                continue


@celery.task
def generate_tips_and_alerts():
    """
    For each user form DB calls methods of generating tips and alerts
    """
    users = User.filter_only(metrics={'$exists': True}, fields={'_id':True, 'auth_token':True})

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
    result = {
        'ga_dates':dates,
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
        for metric_name, value in res.items():
            result[metric_name].update(**value)

    totals_report = generate_report_body(
        view_id=view_id,
        start_date=start_date,
        end_date=end_date,

        metrics=['ga:sessions', 'ga:users', 'ga:pageviews',
        'ga:pageviewsPerSession', 'ga:avgSessionDuration', 'ga:bounces',
        'ga:percentNewSessions', 'ga:pageviews', 'ga:timeOnPage', 'ga:pageLoadTime',
        'ga:avgPageLoadTime', 'ga:transactionsPerSession', 'ga:transactionRevenue'],

        dimensions=['ga:date'])

    totals = google_analytics_query_totals(totals_report, start_date, end_date, token)
    for metric, total in totals.items():
        result[metric]['total']= total

    path = f'users_metrics/{token}'
    if len(dates) > 1:
        if not os.path.exists(path):
            os.makedirs(path)
            metrics = {'google_analytics': result}

        else:
            with open(f'{path}/metrics.json', 'r') as f:
                metrics = json.loads(f.read())
                metrics['google_analytics'] = result

        with open(f'{path}/metrics.json', 'r+') as f:
                f.write(json.dumps(metrics))
    else:
        with open(f'{path}/metrics.json', 'r+') as f:
                all_metrics = json.loads(f.read())
                metrics = all_metrics.pop('google_analytics')
                del all_metrics
                dates = metrics.pop('ga_dates')
                dates.append(result.get('ga_dates')[0])
                if metrics:
                    #This is hella bad
                    for m_name, m_value in metrics.items():
                        for d_name, d_value in m_value.items():
                            for sub_d_name, sb_d_value in d_value.items():
                                # sub d value -> list of metrics
                                sb_d_value.append(
                                    result.get(m_name).get(d_name).get(sub_d_name)[0]
                                )
                    metrics['ga_dates'] = dates
                    # get file second time to shorthen the update period
                    all_metrics = json.loads(f.read())
                    all_metrics['google_analytics'] = metrics
                    f.write(json.dumps(all_metrics))


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


def google_analytics_query_totals(report, start_date, end_date, token):
    api_client = build(serviceName='analyticsreporting', version='v4', http=auth_credentials(token), cache_discovery=False)
    response = api_client.reports().batchGet(
        body={
            'reportRequests': report
        }).execute()

    if response.get('reports')[0].get('data').get('rows'):
        parsed_response = GoogleUtils.GoogleTotalsReportsParser(response).parse()
        parsed_response.pop('ga_dates')
    else:
        l = len(create_list_of_dates(start_date, end_date))
        metrics = ['ga:sessions', 'ga:users', 'ga:pageviews',
                     'ga:pageviewsPerSession', 'ga:avgSessionDuration', 'ga:bounces',
                     'ga:percentNewSessions', 'ga:pageviews', 'ga:timeOnPage', 'ga:pageLoadTime',
                     'ga:avgPageLoadTime', 'ga:transactionsPerSession', 'ga:transactionRevenue']
        parsed_response = {k: [0] * l for k in metrics}

    return parsed_response