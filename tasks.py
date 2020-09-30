import os
from celery import Celery
from Systems.Google.GoogleAnalytics import google_analytics_query, insert_ga_data_in_db
from Utils.GoogleUtils import prep_db_metrics
from user import append_list

from user import query_many

celery_app = Celery('melytix-celery')


@celery_app.task
def refresh_metrics():
    if (mongo_users := query_many(user_type="google_auth")):
        print(mongo_users)
        step = 10
        users = [user for user in mongo_users]  # convert pymongo cursor obj to list
        print(users)
        # refresh 10 users by one task for more threaded performace
        for id in range(0, len(users), step):
	        refresh_metric.delay((users[id: id + step]))


@celery_app.task
def refresh_metric(users: list):
    #TODO: in future make this function refresh all system metrics that user connects
    for user in users:
        print(user)
        token = user['tokens']['g_access_token']
        view_id = user['viewid']

        metrics = google_analytics_query(token, view_id, 'today', 'today')

        insert_dict = prep_db_metrics(ga_data=metrics)
        for key in insert_dict:
            append_list(
                filter={
                    'email': user['email']
                    },
                    key=insert_dict[key]
                )
