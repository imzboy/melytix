import os
from celery import Celery
from config import settings

APP_ENV = os.environ.get('APP_ENV', 'Dev')
config = getattr(settings, f'{APP_ENV}Config')


def make_celery():
   celery = Celery(__name__, broker=config.CELERY_BROKER)
   celery.conf.update(config.as_dict())
   return celery

celery = make_celery()
