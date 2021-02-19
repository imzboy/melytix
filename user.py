from flask_login.mixins import UserMixin
from pymongo import MongoClient
from pymongo.results import InsertOneResult
import os
from hashlib import pbkdf2_hmac
import binascii
import inspect
from bson import ObjectId, objectid

# Connecting to Mogodb Atlas
uri = os.environ.get('MONGODB_URI', None)

client = MongoClient(uri)

database_name = os.environ.get('DATABASE_NAME', None)

db = client.database_name

'''
see Docs/UserDB Structure.txt if there is any questions
'''


class MongoDocument(object):

    def __init__(self, data:dict):
        self.data = data

    @classmethod
    def db(cls):
        return db.__getattr__(f'{cls.__name__.lower()}s')

    @classmethod
    def get(cls, **kwargs):
        if (mongo_data := cls.db().find(kwargs)):
            if mongo_data.count() == 1:
                return cls(mongo_data[0])
            raise Exception(
                f'{cls.__name__}.get() returned more than one element. It returned {mongo_data.count()}!')
        return None

    @classmethod
    def filter(cls, **kwargs):
        """
        Finds all users in db, which matches the filter
            Parameters:
                **kwargs:  parameters for search
        """
        if(mongo_data := cls.db().find(kwargs)):
            return [cls(data) for data in mongo_data]
        return None

    @classmethod
    def create(cls, **kwargs) -> InsertOneResult:
        return cls.db().insert_one(kwargs)

    @classmethod
    def update_one(cls, filter, update):
        """
        Finds and updates user data.
        Function does not insert a new document when no match is found.
            Parameters:
                filter (dict): parameters for user search
                update (dict): updated user`s data
        """
        cls.db().find_one_and_update(
            filter,
            {'$set': update},
            upsert=False
        )

    @classmethod
    def append_list(cls, filter: dict, append: dict):
        """
        Append data to users selected with a filter
            Parameters:
                filter (dict) : parameters for search
                append (dict) : data to append
        """
        cls.db().update_one(
            filter,
            {'$push': append}
        )

    def __getattribute__(self, name: str):
        if name == 'data':
            return object.__getattribute__(self, name)

        return self.data.get(name)

    def __str__(self) -> str:
        return f'<{self.__class__.__name__} {str(self._id)}>'


class User(MongoDocument):
    _id : ObjectId
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

    def __str__(self) -> str:
        return f'<User {self.email}>'

    @classmethod
    def register(cls, email: str, password: str):
        """
        Hashes the password and register one new user in the database.
            Parameters:
                email (str): new user`s email
                password (str): new user`s string representation of password
        """
        salt = os.urandom(24)
        password = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        result = cls.create(email=email, password=password, salt=salt)
        return result

    @classmethod
    def verify_password(cls, email, inputted_pass):
        """
        Hashes and checks the inputted password,
            Parameters:
                email (str): user`s email
                inputted_pass (str): user`s inputted password
        """
        if (user := cls.get({'email': email})):
            salt = user.salt
            if user.password == pbkdf2_hmac(
                'sha256',
                inputted_pass.encode('utf-8'),
                salt,
                100000):
                return True
        return False

    @classmethod
    def get_or_create_token(cls, email) -> str:
        """
        Get or create user's token that is used in every api
        for secure assess. If token was found - return token,
        else - creates and assigns to the user.
        Function does not insert a new document when no match is found.
            Parameter:
                email (str): user`s email
        """
        user = User.get({'email': email})

        if (token := user.auth_token):
            return token

        token = binascii.hexlify(os.urandom(20)).decode()
        db.find_one_and_update(
            {'email': email},
            {'$set': {
                'auth_token': token
            }},
            upsert=False
        )
        return token


class Admin(UserMixin, MongoDocument):
    _id : ObjectId
    email : str
    password : bytes
    salt : bytes

    def __str__(self) -> str:
        return f'<Admin {self.email}>'

    def get_id(self):
        return str(self._id)

    @classmethod
    def verify_password(cls, email, inputted_pass):
        """
        Hashes and checks the inputted password,
            Parameters:
                email (str): user`s email
                inputted_pass (str): user`s inputted password
        """
        if (user := cls.get({'email': email})):
            salt = user.salt
            if user.password == pbkdf2_hmac(
                'sha256',
                inputted_pass.encode('utf-8'),
                salt,
                100000):
                return True
        return False


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
