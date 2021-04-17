from user.base import client

db = client["melytix_db"]
col = db["users"]

col.update_many({}, {'$unset': {'Tips': 1, 'tips': 1, 'Alerts': 1, 'alerts': 1, 'metrics': 1}, '$set': {'language': 'en'}},
                  upsert=True)
