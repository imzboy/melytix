import os
from user.base import client
from config import settings

APP_ENV = os.environ.get('APP_ENV', 'Dev')
config = getattr(settings, f'{APP_ENV}Config')
db_name = config.DATABASE_NAME
db = client[db_name]
col = db["users"]

col.update_many({}, {'$unset': {'Tips': 1, 'tips': 1, 'Alerts': 1, 'alerts': 1, 'metrics': 1}, '$set': {'language': 'en'}},
                  upsert=True)
