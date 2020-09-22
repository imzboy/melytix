import os
import celery

from app import app

celery_app = celery.Celery(
    app.import_name,
    backend=os.environ['CELERY_RESULT_BACKEND'],
    broker=os.environ['BROKER_URL']
)
celery_app.conf.update(app.config)

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask


@celery_app.task
def test():
    print('working')