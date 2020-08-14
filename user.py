import pymongo
import os
from hashlib import pbkdf2_hmac
import binascii

# Connecting to Mogodb Atlas
uri = os.environ.get('MONGODB_URI', None)

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


def get_by_token(token: str):
    user = db.find_one({'auth_token': token})
    if user:
        return user
    return None

def register(email: str, password: str) -> None:
    salt = os.urandom(24)
    password = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    db.insert_one({
        'email': email,
        'password': password,
        'salt': salt,
        'user_type': 'normal'
    })

def register_from_google(email: str, picture: str):
    if db.find_one({'email': email}):
        return None  # the user already exists
    db.insert_one({
        'email': email,
        'picture': picture,
        'user_type': 'google_auth'
    })


def verify_token(token: str) -> bool:
    user = db.find_one({'auth_token': token})
    if user:
        return True
    return False


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
    try:
        token = user['auth_token']
        return token
    except KeyError:
        token = binascii.hexlify(os.urandom(20)).decode()
        db.find_one_and_update(
            {'email': email},
            {'$set': {
                'auth_token': token
            }},
            upsert=False
        )
        return token


def add_scopes(token: str, scope: list):
    """adding scopes for google apis in the database for future usage

    Args:
        token (str): the token that we use to find the user
        scope (list): the scopes that we are adding
    """
    db.find_one_and_update(
        {'auth_token': token},
        {'$set': {
            'SCOPE': scope
        }},
        upsert=False
    )


def insert_viewid(token: str, viewid: str):
    db.find_one_and_update(
        {'auth_token': token},
        {'$set': {
            'viewid': viewid
        }},
        upsert=False
    )


def insert_site_for_sc(token: str, site_url: str):
    db.find_one_and_update(
        {'auth_token': token},
        {'$set': {
            'site_utl': site_url
        }},
        upsert=False
    )


def get_g_tokens(token: str):
    tokens = db.find_one(
        {'auth_token': token}
        ).get('tokens', None)
    if tokens:
        return tokens['g_access_token'], tokens['g_refresh_token']


def insert_tokens(token: str, access_token: str, refresh_token: str):
    """Mongodb find and update func for adding user tokens in db

    Args:
        token: the token that we use to find the user
        access_token: the google access token
        refresh_token: the google refresh token"""
    db.find_one_and_update(
        {'auth_token': token},
        {'$set': {
            'tokens': {'g_access_token': access_token,
                       'g_refresh_token': refresh_token}
        }},
        upsert=False
    )
