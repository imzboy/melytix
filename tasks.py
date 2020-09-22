import os
import celery


celery_app = celery.Celery(
    'melytix-celery',
    backend=os.environ['REDIS_URL'],
    broker=os.environ['REDIS_URL']
)

@celery_app.task
def test():
    print('working')