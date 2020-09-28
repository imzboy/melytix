import os

#periodic tasks
celery_beat_schedule = {
    "time_scheduler": {
        "task": "tasks.refresh_metrics",
        "schedule": 30.0,
    }
}

#celery and beat configurations
broker_uri = os.environ.get('REDIS_URL')

result_backend = os.environ.get('REDIS_URL')

timezone = 'Europe/Kiev'

imports = ('tasks',)

task_serializer="json"

accept_content=["json"]

result_serializer="json"

beat_schedule=celery_beat_schedule
