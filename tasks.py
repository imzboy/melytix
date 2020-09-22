import os
import celery


celery_app = celery.Celery(
    'melytix-celery',
    backend=os.environ['CELERY_RESULT_BACKEND'],
    broker=os.environ['BROKER_URL']
)

@celery_app.task
def test():
    print('working')