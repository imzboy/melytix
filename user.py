from typing import Any
from flask_login.mixins import UserMixin
from pymongo import MongoClient
from pymongo.results import InsertOneResult
import os
from hashlib import pbkdf2_hmac
import binascii
from bson import ObjectId


# Connecting to Mogodb Atlas
uri = os.environ.get('MONGODB_URI', None)

client = MongoClient(uri)

db_name = os.environ.get('DATABASE_NAME')

'''
see Docs/UserDB Structure.txt if there is any questions
'''


class MongoDocument(object):

    def __init__(self, data : dict):
        self.data = data

    @classmethod
    def db(cls):
        return client.__getattr__(db_name).__getattr__(f'{cls.__name__.lower()}s')

    @classmethod
    def get(cls, **kwargs):
        if (mongo_data := cls.db().find(kwargs)):
            if mongo_data.count() == 1:
                return cls(mongo_data[0])
            raise Exception(
                f'{cls.__name__}.get() returned more than one element.'\
                f'It returned {mongo_data.count()}!')
        return None

    def exists(cls, **kwargs) -> bool:
        return bool(cls.db().find_one(kwargs))

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

    def __getattribute__(self, name: str):
        if name == 'data':
            return object.__getattribute__(self, name)

        if (attr := self.data.get(name, {})): #TODO: bad...
            return attr

        return None

    def __setattr__(self, name: str, value):

        if name == 'data':
            object.__setattr__(self, name, value)
        else:
            self.data.update({name: value})

    @property
    def dict(self):
        return self.data


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
        return self.email

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
        if (user := User.get(email=email)):
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
        user = User.get(email=email)

        if (token := user.auth_token):
            return token

        token = binascii.hexlify(os.urandom(20)).decode()
        User.update_one(
            {'email': email},
            {'auth_token': token})
        return token

    @classmethod
    def get_g_tokens(cls, token: str):
        """
        Secures access by token and finds tokens
        for Google api access and refresh token.
            Parameter:
                token (str): the token that we use to find the user
        """
        tokens = User.get(auth_token=token).tokens
        if tokens:
            return tokens['g_access_token'], tokens['g_refresh_token']
        return None

    @classmethod
    def insert_tokens(cls, token: str, access_token: str, refresh_token: str):
        """
        Mongodb find and update func for adding user tokens in db
        Function does not insert a new document when no match is found.
            Parameters:
                token (str): the token that we use to find the user
                access_token (str): the google access token
                refresh_token (str): the google refresh token
        """
        User.update_one(
            {'auth_token': token},
            {'tokens': {'g_access_token': access_token,
                        'g_refresh_token': refresh_token}}
        )

    @classmethod
    def f_insert_tokens(cls, token: str, access_token: str):
        """
        Insert facebook access_token in db

            Args:
            token: the token that we use to find the user
            access_token: the facebook access token
        """
        User.update_one(
            {'auth_token': token},
            {'tokens': {'f_access_token': access_token}})

    @classmethod
    def insert_dash_settings(cls, token: str, settings: dict):
        """
        Inserts new user settings for his dashboard.
        Function does not insert a new document when no match is found.
            Parameters:
                token (str) : the token that we use to find the user
                settings (str) : new user settings for his dashboard
        """
        User.update_one(
            {'auth_token': token},
            {'DashSettings': settings})

    @classmethod
    def insert_data_in_db(cls, token: str, system: str, data: dict):
        User.update_one(
            {'auth_token': token},
            {f'metrics.{system}': data})

    @classmethod
    def connect_system(cls, token: str, system: str, data: dict):
        User.update_one(
            {'auth_token': token},
            {f'connected_systems.{system}': data})

    @classmethod
    def flip_tip_or_alert(cls, token: str, type_: str, id_: str):
        user = User.get(auth_token=token)
        list_of_data = user.dict.get(f'{type_}s')

        for item in list_of_data:
            if item.get('id') == id_:
                item.update({'active': not item.get('active')})

        User.update_one(
            {'auth_token': token},
            {f'{type_}s': list_of_data})


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
