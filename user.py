from flask_login.mixins import UserMixin
from pymongo import MongoClient
import os
from hashlib import pbkdf2_hmac
import binascii
import inspect
from bson import ObjectId

# Connecting to Mogodb Atlas
uri = os.environ.get('MONGODB_URI', None)

client = MongoClient(uri)

db = client.heroku_t2hftlhq

'''
see Docs/UserDB Structure.txt if there is any questions
'''

class MongoDocument(object):
    _id : ObjectId

    def __init__(self, **fields):
        self.db_connection = client.heroku_t2hftlhq.__getattr__(f'{self.__class__.__name__.lower()}s')
        self.attributes: dict = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))[0][1]

        for field_name, field_value in fields.values():

            if not field_name in self.attributes.keys():
                raise Exception(f'The {self.__class__.__name__} does not have field {field_name}')

            if isinstance(field_value, self.attributes.get(field_name)):
                self.__setattr__(field_name, field_value)

    def query(self, **kwargs):
        if (mongo_data := db.find_one(kwargs)):
            return self.__class__(mongo_data)
        return None

    def query_many(self, **kwargs):
        """
        Finds all users in db, which matches the filter
            Parameters:
                **kwargs:  parameters for users search
        """
        if(mongo_data := db.find(kwargs)):
            return [self.__class__(data) for data in mongo_data]
        return None

    def save(self):
        if self.query(_id=self._id):
            db.find_one_and_update(
                {"_id":self._id},
                {'$set': self.__dict__},
                upsert=False
            )
        else:
            db.insert


class User(MongoDocument):
    email : str
    password : bytes
    salt : bytes
    auth_token : str
    tokens : dict
    connected_systems : dict
    metrics : dict
    Tips : list
    Alerts : list
    DashSettings : dict


def query(**kwargs):
    """
    Finds one user in db, which matches the filter
        Parameters:
            **kwargs:  parameters for user search
    """
    if (user := db.find_one(kwargs)):
        return user
    return None


def query_many(**kwargs):
    """
    Finds all users in db, which matches the filter
        Parameters:
            **kwargs:  parameters for users search
    """
    if(user := db.find(kwargs)):
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
    """
    Append data to users selected with a filter
        Parameters:
            filter (dict) : parameters for users search
            append (dict) : data to append
    """
    db.update_one(
        filter,
        {'$push': append}
    )

def find_and_update(filter, update):
    """
    Finds and updates user data.
    Function does not insert a new document when no match is found.
        Parameters:
            filter (dict): parameters for user search
            update (dict): updated user`s data
    """
    db.find_one_and_update(
        filter,
        {'$set': update},
        upsert=False
    )

def register(email: str, password: str) -> None:
    """
    Hashes the password and register one new user in the database.
        Parameters:
            email (str): new user`s email
            password (str): new user`s string representation of password
    """
    salt = os.urandom(24)
    password = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    db.insert_one({
        'email': email,
        'password': password,
        'salt': salt,
    })

def register_from_google(email: str, picture: str):
    """
    Registers a user using data taken from Google.
        Parameters:
            email (str): new user`s email
            picture (str):  user picture
    """
    if db.find_one({'email': email}):
        return None  # the user already exists
    db.insert_one({
        'email': email,
        'picture': picture,
        'user_type': 'google_auth'
    })


def verify_password(email, inputted_pass):
    """
    Hashes and checks the inputted password,
    if user was not found  - throw exception 404
        Parameters:
            email (str): user`s email
            inputted_pass (str): user`s inputted password
    """
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
    """
    Get or create user's token that is used in every api
     for secure assess. If token was found - return token,
     else - creates and assigns to the user.
     Function does not insert a new document when no match is found.
        Parameter:
            email (str): user`s email
    """
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
    """
    Adding scopes for google apis in the database for future usage.
    Function does not insert a new document when no match is found.
        Parameters:
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

def get_g_tokens(token: str):
    """
    Secures access by token and finds tokens
    for Google api access and refresh token.
        Parameter:
            token (str): the token that we use to find the user
    """
    tokens = db.find_one(
        {'auth_token': token}
        ).get('tokens', None)
    if tokens:
        return tokens['g_access_token'], tokens['g_refresh_token']
    return None


def insert_tokens(token: str, access_token: str, refresh_token: str):
    """
    Mongodb find and update func for adding user tokens in db
    Function does not insert a new document when no match is found.
        Parameters:
            token (str): the token that we use to find the user
            access_token (str): the google access token
            refresh_token (str): the google refresh token
    """
    db.find_one_and_update(
        {'auth_token': token},
        {'$set': {
            'tokens': {'g_access_token': access_token,
                       'g_refresh_token': refresh_token}
        }},
        upsert=False
    )


def f_insert_tokens(token: str, access_token: str):
    """
    Insert facebook access_token in db

        Args:
        token: the token that we use to find the user
        access_token: the facebook access token
    """
    db.find_one_and_update(
        {'auth_token': token},
        {'$set': {
            'tokens': {'f_access_token': access_token}
        }},
        upsert=False
    )


def insert_dash_settings(token: str, settings: dict):
    """
    Inserts new user settings for his dashboard.
    Function does not insert a new document when no match is found.
        Parameters:
             token (str) : the token that we use to find the user
             settings (str) : new user settings for his dashboard
    """
    db.find_one_and_update(
        {'auth_token': token},
        {'$set': {
            'DashSettings': settings
        }},
        upsert=False
    )


def insert_data_in_db(token: str, system: str, data: dict):
    db.find_one_and_update(
        {'auth_token': token},
        {'$set': {
            f'metrics.{system}': data
        }},
        upsert=False
    )


def connect_system(token: str, system: str, data: dict):
    db.find_one_and_update(
        {'auth_token': token},
        {'$set': {
            f'connected_systems.{system}': data
        }},
        upsert=False
    )


def flip_tip_or_alert(token: str, type_: str, id_: str):
    user = query(auth_token=token)
    list_of_data = user.get(f'{type_}s')

    for item in list_of_data:
        if item.get('id') == id_:
            item.update({'active': not item.get('active')})

    db.find_one_and_update(
        {'auth_token': token},
        {'$set':
             {f'{type_}s': list_of_data}
         }
    )


class Admin(UserMixin):
    def __init__(self, user_dict: dict):
        self.user_dict = user_dict

    def get_id(self):
        object_id = self.user_dict.get('_id')
        return str(object_id)
