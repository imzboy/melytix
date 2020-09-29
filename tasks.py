import os
from celery import Celery
from Systems.Google.GoogleAnalytics import google_analytics_query

from user import query

celery_app = Celery('melytix-celery')


@celery_app.task
def refresh_metrics():
    if (users := query()):
        step = 10
        # refresh 10 users by one task for more threaded performace
        for id in range(0, len(users), step):
	        refresh_metric.delay((users[id: id + step]))


@celery_app.task
def refresh_metric(users: list):
    for user in users:
        token = user['tokens']['g_access_token']
        view_id = user['viewid']
        metrics = google_analytics_query(token, view_id, 'yesterday', 'today')

