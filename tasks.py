import os
from celery import Celery
from Systems.Google.GoogleAnalytics import google_analytics_query
from Utils.GoogleUtils import prep_db_metrics
from user import append_list

from user import query_many

from Alerts.Alerts import return_alerts

celery_app = Celery('melytix-celery')


@celery_app.task
def refresh_metrics():
    if (mongo_users := query_many(user_type="google_auth")):
        step = 10
        users = []  # convert pymongo cursor obj to list
        for user in mongo_users:
            users.append(
                {'email': user['email'],
                 'token': user['auth_token'],
                 'view_id': user['viewid']})

        # refresh 10 users by one task for more threaded performace
        for id in range(0, len(users), step):
	            refresh_metric.delay((users[id: id + step]))
	        # refresh_metric.delay((users[id: id + step]))


@celery_app.task
def refresh_metric(users: list):
    #TODO: in future make this function refresh all system metrics that user connects
    for user in users:
        print(user)
        token = user['token']
        view_id = user['view_id']

        metrics = google_analytics_query(token, view_id, 'today', 'today')

        insert_dict = prep_db_metrics(ga_data=metrics)
        for key in insert_dict:
            append_list(
                filter={
                    'email': user['email']
                    },
                append={
                    f'G_Analytics.ga_data.{key}': insert_dict[key]
                    }
                )


@celery_app.task
def generate_tips():
    if (mongo_users := query_many()):
        pass


@celery_app.task
def generate_alert(users: list):
    for user in users:
        for alert in return_alerts():
            if alert.analytics_func(user['metrics']):
                append_list(
                    {'email': user['email']},
                    {"Alerts": alert.generate()})


@celery_app.task
def generate_alerts():
    if (mongo_users := query_many()):
        users = []
        for user in mongo_users:
            users.append(
                {'email': user['email'],
                'metrics': user['G_Analytics.ga_data']}
            )

        for id in range(0, len(users), 10):
	            # generate_alert.delay((users[id: id + 10]))
                generate_alert((users[id: id + 10]))
