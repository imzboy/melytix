from celery.schedules import crontab

celery_beat_schedule = {
    "refresh_metrics": {
        "task": "tasks.tasks.refresh_metrics",
        "schedule": crontab(hour=22, minute=0),
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

    MONGODB_URI='mongodb://127.0.0.1:27017'
    DATABASE_NAME='test_db'

    # MONGODB_URI='mongodb+srv://MaxTeslya:7887334Mna@melytixdata.ryedw.mongodb.net/melytix_db?retryWrites=true&w=majority'
    # DATABASE_NAME='melytix_db'

    timezone = 'Europe/Kiev'
    imports = ('tasks.tasks',)
    task_serializer="json"
    accept_content=["json"]
    result_serializer="json"


class ProdConfig(BaseConfig):

    ENV = 'production'

    CELERY_BROKER='redis://127.0.0.1:6379'
    result_backend='redis://127.0.0.1:6379'

    MONGODB_URI='mongodb+srv://MaxTeslya:7887334Mna@melytixdata.ryedw.mongodb.net/melytix_db?retryWrites=true&w=majority'
    DATABASE_NAME='melytix_db'

    #celery and beat configurations
    timezone = 'Europe/Kiev'
    imports = ('tasks.tasks',)
    task_serializer="json"
    accept_content=["json"]
    result_serializer="json"
    beat_schedule=celery_beat_schedule


class StageConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True

    CELERY_BROKER='redis://h:pf0b2c9e78a670264f0b75b20a33311122bdef5f1d0eae7feca0fc74208319647@ec2-34-252-177-9.eu-west-1.compute.amazonaws.com:9279'
    result_backend='redis://h:pf0b2c9e78a670264f0b75b20a33311122bdef5f1d0eae7feca0fc74208319647@ec2-34-252-177-9.eu-west-1.compute.amazonaws.com:9279'

    MONGODB_URI='mongodb+srv://MaxTeslya:7887334Mna@melytixdata-ryedw.mongodb.net/test?retryWrites=true&w=majority'
    DATABASE_NAME='heroku_t2hftlhq'

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
   # make celery execute tasks synchronously in the same process
   CELERY_ALWAYS_EAGER = True
