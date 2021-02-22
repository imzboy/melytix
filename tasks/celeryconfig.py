
from celery.schedules import crontab

# periodic tasks
celery_beat_schedule = {
    "refresh_metrics": {
        "task": "tasks.tasks.refresh_metrics",
        "schedule": crontab(hour=22, minute=0),
    }
}

