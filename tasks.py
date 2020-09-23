import os
from celery import Celery
from celery.schedules import crontab

from user import test_task

celery_app = Celery(
    'melytix-celery',
    backend=os.environ['REDIS_URL'],
    broker=os.environ['REDIS_URL']
)

@celery_app.task
def refresh_metrics():
    test_task()
