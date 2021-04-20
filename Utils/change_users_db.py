import os
from user.base import client
from config import settings

APP_ENV = os.environ.get('APP_ENV', 'Dev')
config = getattr(settings, f'{APP_ENV}Config')
db_name = config.DATABASE_NAME
db = client[db_name]
col = db["users"]

col.update_many({}, {'$unset': {'Tips':  '', 'tips': '', 'Alerts': '', 'alerts': '', 'metrics': ''}, '$set': {'language': 'en'}},
                  upsert=True)
