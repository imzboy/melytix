import os
from celery import Celery
from celery.schedules import crontab

from user import test_task

celery_app = Celery(
    'melytix-celery',
    backend=os.environ['REDIS_URL'],
    broker=os.environ['REDIS_URL']
)

@celery_app.on_after_configure.connect
def send_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, refresh_metrics.delay(), name='add every 10')

@celery_app.task
def refresh_metrics():
    test_task()
