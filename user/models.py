from typing import Any
from user.base import MongoDocument
from flask_login.mixins import UserMixin

import os
from hashlib import pbkdf2_hmac
import binascii

'''
see Docs/UserDB Structure.txt if there is any questions
'''


class User(MongoDocument):
    email : str
    password : bytes
    salt : bytes
    auth_token : str
    tokens : dict
    connected_systems : dict
    metrics : dict
    tips : list
    alerts : list
    dash_settings : dict

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
        result = User.create(email=email, password=password, salt=salt)
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
            {'dash_settings': settings})

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
