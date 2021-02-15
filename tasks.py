import datetime

from celery import Celery

from Alerts.Alerts import return_alerts
from Systems.Facebook.FacebookAdsManager import facebook_insights_query
from Systems.Google.GoogleAnalytics import generate_report_body
from Systems.Google.GoogleAuth import auth_credentials
from Tips.Tips import return_tips
from Utils.GoogleUtils import GoogleReportsParser
from Utils.FacebookUtils import create_list_of_dates
from user import append_list, query_many, insert_data_in_db
from googleapiclient.discovery import build



celery_app = Celery('melytix-celery')


@celery_app.task
def refresh_metrics():
    """
    Makes list of users from DB and calls method for refreshing metrics
    for 10 users by one task
    """
    if (mongo_users := query_many(metrics={'$exists': True})):
        users = []  # convert pymongo cursor obj to list
        for user in mongo_users:
            if user.get('connected_systems', {}).get("google_analytics", {}).get(
                    'viewid'):  # TODO: change when db is stable again
                users.append(
                    {'email': user['email'],
                     'token': user['auth_token'],
                     'view_id': user['connected_systems']['google_analytics']['viewid']})

        # refresh 10 users by one task for more threaded performace
        step = 10
        for id in range(0, len(users), step):
            refresh_metric((users[id: id + step]))
            # refresh_metric.delay((users[id: id + step]))


@celery_app.task
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
        view_id = user['view_id']

        google_analytics_query_all.delay(token, view_id, 'today', 'today')

        today = datetime.datetime.now()
        f_metrics = facebook_insights_query(token, today, today)
        for campaign, metrics in f_metrics.items():
            for metric, value in metrics.items():
                append_list(
                    filter={
                        'email': user['email']
                    },
                    append={f'metrics.facebook_insights.{campaign}.{metric}': {'$each': value}}
                )


@celery_app.task
def generate_tip(users: list):
    """
    Adds tips to the DB for each user from the list if their analytics_func returns True
            Parameters:
                users (list): list of users to check metrics of user
    """
    for user in users:
        for tip in return_tips():
            if tip.analytics_func(user['metrics']):
                append_list(
                    {'email': user['email']},
                    {"Tips": tip.generate()})


@celery_app.task
def generate_alert(users: list):
    """
    Adds alerts to the DB for each user on the list according to their traffic
                Parameters:
                users (list): list of users to check traffic
    """
    for user in users:
        for alert in return_alerts():
            if alert.analytics_func(user['metrics']):
                append_list(
                    {'email': user['email']},
                    {"Alerts": alert.generate()})


@celery_app.task
def generate_tips_and_alerts():
    """
    For each user form DB calls methods of generating tips and alerts
    """
    if (mongo_users := query_many()):
        users = []
        for user in mongo_users:
            if user.get('metrics').get('google_analytics'):  # TODO: change this when more systems will be added
                users.append(
                    {'email': user['email'],
                     'metrics': user['metrics']['google_analytics']}
                )

        for id in range(0, len(users), 10):
            # generate_alert.delay((users[id: id + 10]))
            generate_alert((users[id: id + 10]))
            # generate_tip.delay((users[id: id + 10]))
            generate_tip((users[id: id + 10]))


@celery_app.task
def google_analytics_query_all(token, view_id, start_date, end_date):
    # Max of 10 metrics and 7 dimesions in one report body
    dimensions = ['ga:browser', 'ga:browserVersion', 'ga:operatingSystem',
                  'ga:browser', 'ga:browserVersion', 'ga:operatingSystemVersion',
                  'ga:mobileDeviceBranding', 'ga:mobileInputSelector', 'ga:mobileDeviceModel',
                  'ga:mobileDeviceInfo', 'ga:deviceCategory', 'ga:browserSize', 'ga:country',
                  'ga:region', 'ga:city', 'ga:language', 'ga:userAgeBracket', 'ga:userGender',
                  'ga:interestOtherCategory']
    for dimension in dimensions:

        report = generate_report_body(
            view_id=view_id,
            start_date=start_date,
            end_date=end_date,

            metrics=['ga:sessions', 'ga:users', 'ga:pageviews',
                     'ga:pageviewsPerSession', 'ga:avgSessionDuration', 'ga:bounces',
                     'ga:percentNewSessions', 'ga:pageviews', 'ga:timeOnPage', 'ga:pageLoadTime',
                     'ga:avgPageLoadTime', 'ga:transactionsPerSession', 'ga:transactionRevenue'],

            dimensions=['ga:date', dimension])
        google_analytics_query.delay(report, start_date, end_date, token)


@celery_app.task
def google_analytics_query(report: list, start_date, end_date, token):
    # Google Analytics v4 api setup to make a request to google analytics
    api_client = build(serviceName='analyticsreporting', version='v4', http=auth_credentials(token))
    response = api_client.reports().batchGet(
        body={
            'reportRequests': report
        }).execute()

    dates = create_list_of_dates(start_date, end_date)

    parsed_response = GoogleReportsParser(response, dates).parse()
    for metric, metric_value in parsed_response.items():
        # if this is the first request to GA
        if len(dates) > 1:
            insert_data_in_db(token, f'google_analytics.{metric}', metric_value)
            append_list(token, {f'metrics.google_analytics.ga_dates': dates})

        # everyday request
        else:
            for dimension, dimension_value in metric_value.items():
                for sub_dimension, value in dimension_value.items():
                    append_list(
                        filter={
                            'auth_token': token
                        },
                        append={
                            f'metrics.google_analytics.{dimension}.{sub_dimension}': value if isinstance(value, int) else value[0]
                        }
                    )
            # append date
            append_list(token, {'metrics.google_analytics.ga_dates': dates[0]})









