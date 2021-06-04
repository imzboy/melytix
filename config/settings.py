from celery.schedules import crontab

celery_beat_schedule = {
    "refresh_metrics": {
        "task": "tasks.tasks.refresh_metrics",
        "schedule": crontab(hour=20, minute=0),
    },
    "generate_tips_and_alerts": {
        "task": "tasks.tasks.generate_tips_and_alerts",
        "schedule": crontab(hour=22, minute=0),
    },
    "check_accounts_for_delete": {
        "task": "tasks.tasks.check_accounts_for_delete",
        "schedule": crontab(hour=1, minute=0),
    }
}



class BaseConfig(object):
    TESTING = False
    DEBUG = False

    @classmethod
    def as_dict(cls):
        res = {f:getattr(cls, f) for f in dir(cls) if not '__' in f}
        return res


class DevConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True

    CELERY_BROKER='redis://127.0.0.1:6379'
    result_backend='redis://127.0.0.1:6379'

    MONGODB_URI='mongodb+srv://MaxTeslya:7887334Mna@melytixdata.ryedw.mongodb.net/melytix_db?retryWrites=true&w=majority'
    DATABASE_NAME='melytix_db'

    PROTOCOL = 'https'

    FRONT_URL = 'https://systemdev.melytix.com'

    DOMAIN = 'dev.melyback.tk'

    timezone = 'Europe/Kiev'
    imports = ('tasks.tasks',)
    task_serializer="json"
    accept_content=["json"]
    result_serializer="json"


class ProdConfig(BaseConfig):

    ENV = 'production'

    CELERY_BROKER='redis://127.0.0.1:6379'
    result_backend='redis://127.0.0.1:6379'

    MONGODB_URI='mongodb+srv://MaxTeslya:7887334Mna@melytixdata.ryedw.mongodb.net/melytix_prod_db?retryWrites=true&w=majority'
    DATABASE_NAME='melytix_prod_db'

    PROTOCOL = 'https'

    FRONT_URL = 'https://system.melytix.com'

    DOMAIN = 'melyback.tk'

    #celery and beat configurations
    timezone = 'Europe/Kiev'
    imports = ('tasks.tasks',)
    task_serializer="json"
    accept_content=["json"]
    result_serializer="json"
    beat_schedule=celery_beat_schedule


class TestConfig(BaseConfig):
    ENV = 'development'
    TESTING = True
    DEBUG = True
    ENV = 'development'
    DEBUG = True

    PROTOCOL = 'http'

    CELERY_BROKER='redis://127.0.0.1:6379'
    result_backend='redis://127.0.0.1:6379'

    MONGODB_URI='mongodb+srv://MaxTeslya:7887334Mna@melytixdata.ryedw.mongodb.net/melytix_db?retryWrites=true&w=majority'
    DATABASE_NAME='melytix_db'

    FRONT_URL = 'https://systemdev.melytix.com'

    DOMAIN = '127.0.0.1:5000'

    timezone = 'Europe/Kiev'
    imports = ('tasks.tasks',)
    task_serializer="json"
    accept_content=["json"]
    result_serializer="json"

    # make celery execute tasks synchronously in the same process
    CELERY_ALWAYS_EAGER = True


class JiraConfig:
    LOGIN = 'nicknamebos0@gmail.com'
    API_KEY = 'HNWRpbO8mvpCY2SahmTdD815'
    BOARD_NAME = 'DEV board'
    SPRINT_NAME = 'DEV Sprint 1'
    TRANSITION_NAME = 'Task that has to be done'
