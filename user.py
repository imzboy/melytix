from flask_login.mixins import UserMixin
from pymongo import MongoClient
import os
from hashlib import pbkdf2_hmac
import binascii


# Connecting to Mogodb Atlas
uri = os.environ.get('MONGODB_URI', None)

client = MongoClient(uri)

db = client.heroku_t2hftlhq.users

'''
see Docs/UserDB Structure.txt if there is any questions
'''

def query(**kwargs):
    if (user := db.find_one(kwargs)):
        return user
    return None


def query_admin(**kwargs):
    db = client.heroku_t2hftlhq.admins
    if (user := db.find_one(kwargs)):
        return user
    return None


def query_many(**kwargs):
    if(users := db.find(kwargs)):
        return users
    return None


def append_list(filter: dict, append: dict):
    db.update_one(
        filter,
        {'$push': append}
    )

def find_and_update(filter, update):
    db.find_one_and_update(
        filter,
        {'$set': update},
        upsert=False
    )

def register(email: str, password: str) -> None:
    salt = os.urandom(24)
    password = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    db.insert_one({
        'email': email,
        'password': password,
        'salt': salt,
    })

def register_from_google(email: str, picture: str):
    if db.find_one({'email': email}):
        return None  # the user already exists
    db.insert_one({
        'email': email,
        'picture': picture,
        'user_type': 'google_auth'
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


def verify_admin_password(email, inputted_pass):
    db = client.heroku_t2hftlhq.admins
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
    if (token := user.get('auth_token')):
        return token
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
            'connected_systems.google_analytics.viewid': viewid
        }},
        upsert=False
    )


def insert_site_for_sc(token: str, site_url: str):
    db.find_one_and_update(
        {'auth_token': token},
        {'$set': {
            'connected_systems.search_console.site_utl': site_url
        }},
        upsert=False
    )


def get_g_tokens(token: str):
    tokens = db.find_one(
        {'auth_token': token}
        ).get('tokens', None)
    if tokens:
        return tokens['g_access_token'], tokens['g_refresh_token']
    return None


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


def insert_dash_settings(token: str, settings: dict):
    db.find_one_and_update(
        {'auth_token': token},
        {'$set': {
            'DashSettings': settings
        }},
        upsert=False
    )


def flip_tip_or_alert(token: str, type_: str, id: str):
    user = db.find_one(
        {'auth_token': token,
         f'{type_}s.id': {id}}
        )

    algorithms_res = user.get(f'{type_}s')
    alg_bool = False

    for alg in algorithms_res:
        if alg.get('id') == id:
            alg_bool = alg.get('active')


    db.update_one(
        {'auth_token': token,
        f'{type_}s.id': {id}},
        {'$set': {
            f'{type_}s.$.active': not alg_bool
        }}
    )


class Admin(UserMixin):
    def __init__(self, user_dict: dict):
        self.user_dict = user_dict

    def get_id(self):
        object_id = self.user_dict.get('_id')
        return str(object_id)
