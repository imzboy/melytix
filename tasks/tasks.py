from Systems.Google.views import search_console_metrics
from Systems.Google.SearchConsole import make_sc_request
import celery
from Utils import GoogleUtils
from analytics.base import MetricAnalyzer, MetricNotFoundException
from Utils.utils import inheritors
import datetime

from Systems.Facebook.FacebookAdsManager import facebook_insights_query
from Systems.Google.GoogleAnalytics import generate_report_body
from Systems.Google.GoogleAuth import auth_credentials
from Utils.GoogleUtils import GoogleReportsParser, fill_all_with_zeros
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
        users = []  # convert pymongo cursor obj to list
        for mongo_user in mongo_users:
            user = {'email': user['email'],
                'token': user['auth_token']}
            if user.connected_systems.get('google_analytics'):  #TODO: add more systems
                user['view_id'] = mongo_user['connected_systems']['google_analytics']['viewid']
            if user.connected_systems.get('search_console'):
                user['site_url'] = mongo_user['connected_systems']['search_console']['site_url']

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
            today = datetime.datetime.now().date().isoformat()
            response = make_sc_request(token, site_url, today, today)
            data = GoogleUtils.prep_dash_metrics(sc_data=response)
            for key, value in data.items():
                User.append_list({'auth_token': token}, {f'metrics.search_console.{key}': value[0]})

        # f_metrics = facebook_insights_query(token, today, today)
        # for campaign, metrics in f_metrics.items():
        #     for metric, value in metrics.items():
        #         User.append_list(
        #             {'email': user['email']},
        #             {f'metrics.facebook_insights.{campaign}.{metric}': {'$each': value}}
        #         )


@celery.task
def generate_tip_or_alert(users:list):
    analytics = inheritors(MetricAnalyzer)
    for user in users:
        for analytics_class in analytics:
            try:
                analytics_class(user.get('metrics')).analyze(user.get('_id'))
            except MetricNotFoundException:
                continue

@celery.task
def generate_tips_and_alerts():
    """
    For each user form DB calls methods of generating tips and alerts
    """
    users = User.filter_only(metrics={'$exists': True}, fields={'_id':True, 'metrics':True})
    step = 10
    for i in range(0, len(users), step):
        generate_tip_or_alert.delay(users[i:i+step])


@celery.task
def google_analytics_query_all(token, view_id, start_date, end_date):
    # Max of 10 metrics and 7 dimesions in one report body
    dimensions = ['ga:browser', 'ga:operatingSystem',
                  'ga:operatingSystemVersion', 'ga:mobileDeviceBranding',
                  'ga:mobileInputSelector', 'ga:mobileDeviceModel',
                  'ga:mobileDeviceInfo', 'ga:deviceCategory', 'ga:browserSize', 'ga:country',
                  'ga:region', 'ga:language', 'ga:userAgeBracket', 'ga:userGender',
                  'ga:interestOtherCategory', 'ga:city']
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
        dates = create_list_of_dates(start_date, end_date)
        User.insert_data_in_db(token, f'google_analytics.ga_dates', dates)
        google_analytics_query.delay(report, start_date, end_date, token)


@celery.task
def google_analytics_query(report: list, start_date, end_date, token):
    # Google Analytics v4 api setup to make a request to google analytics
    api_client = build(serviceName='analyticsreporting', version='v4', http=auth_credentials(token), cache_discovery=False)
    response = api_client.reports().batchGet(
        body={
            'reportRequests': report
        }).execute()

    dates = create_list_of_dates(start_date, end_date)

    if response.get('reports')[0].get('data').get('rows'):
        parsed_response = GoogleReportsParser(response, dates).parse()
    else:
        parsed_response = fill_all_with_zeros(response, dates)
    for metric, metric_value in parsed_response.items():
        # if this is the first request to GA
        if len(dates) > 1:
            for dimension, dimension_value in metric_value.items():
                User.insert_data_in_db(token, f'google_analytics.{metric}.{dimension}', dimension_value)

        # everyday request
        else:
            for dimension, dimension_value in metric_value.items():
                for sub_dimension, value in dimension_value.items():
                    User.append_list(
                        filter={
                            'auth_token': token
                        },
                        append={
                            f'metrics.google_analytics.{dimension}.{sub_dimension}': value if isinstance(value, int) else value[0]
                        }
                    )
            # append date
            User.append_list(token, {'metrics.google_analytics.ga_dates': dates[0]})









