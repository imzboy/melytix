import os
from celery import Celery
from Systems.Google.GoogleAnalytics import google_analytics_query
from Systems.Facebook.FacebookAdsManager import facebook_insights_query
from Utils.GoogleUtils import GoogleReportsParser
from user import append_list
import datetime

from user import query_many

from Alerts.Alerts import return_alerts
from Tips.Tips import return_tips

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
            if user.get('connected_systems', {}).get("google_analytics", {}).get('viewid'):  # TODO: change when db is stable again
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
    #TODO: in future make this function refresh all system metrics that user connects
    for user in users:
        token = user['token']
        view_id = user['view_id']

        metrics = google_analytics_query(token, view_id, 'today', 'today')

        insert_dict = GoogleReportsParser(metrics).parse()
        for key, value in insert_dict.items():
            append_list(
                filter={
                    'email': user['email']
                    },
                append={
                    f'metrics.google_analytics.{key}': value if isinstance(value, int) else value[0]
                    }
                )

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
        if (user_metrics := user.get('metrics', {}).get('google_analytics')):
            for alert in return_alerts():
                if alert.analytics_func(user_metrics):
                    alert.format(user_metrics, 'title')
                    alert.format(user_metrics, 'description')
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
