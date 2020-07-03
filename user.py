import pymongo
import os
from hashlib import pbkdf2_hmac
import binascii

# Connecting to Mogodb Atlas
uri = os.environ.get('MONGODB_URI', None)
collection = pymongo.MongoClient(uri)

client = pymongo.MongoClient(uri)

db = client.heroku_t2hftlhq.users

def get_by_email(email: str):
    user = db.find_one({'email': email})
    if user:
        return user
    return None


def get_by_id(user_id):
    user = db.find_one({'_id': user_id})
    if user:
        return user
    return None


def register(email: str, password: str) -> None:
    salt = os.urandom(24)
    password = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    db.insert_one({
        'email': email,
        'password': password,
        'salt': salt
    })


def verify_password(email, inputted_pass):
    user = db.find_one({'email': email})
    if user:
        salt = user['salt']
        inputted_pass = pbkdf2_hmac(
            'sha256',
            inputted_pass.encode('utf-8'),
            salt,
            100000)
        if user['password'] == inputted_pass:
            return True
        else:
            return False
    else:
        return 404


def get_or_create_token(email):
    user = db.find_one({'email': email})
    if user['auth_token']:
        return user['auth_token']
    else:
        token = binascii.hexlify(os.urandom(20)).decode()
        db.find_one_and_update(
            {'email': email},
            {'$set': {
                'auth_token': token
            }},
            upsert=False
        )
        return token


def add_scopes(email: str, scope: list):
    """adding scopes for google apis in the database for future usage

    Args:
        email (str): the email that we use to find the user
        scope (list): the scopes that we are adding
    """
    db.find_one_and_update(
        {'email': email},
        {'$set': {
            'SCOPE': scope
        }},
        upsert=False
    )


def insert_tokens(email: str, access_token: str, refresh_token: str):
    """Mongodb find adn update func for adding user tokens in db

    Args:
        email: the email that we use to find the user
        access_token: the google access token
        refresh_token: the google refresh token"""
    db.find_one_and_update(
        {'email': email},
        {'$set': {
            'tokens': {'g_access_token': access_token,
                        'g_refresh_token': refresh_token}
        }},
        upsert=False
    )
