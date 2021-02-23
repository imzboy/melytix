import os
from pymongo import MongoClient
from pymongo.results import InsertOneResult
from bson import ObjectId
from datetime import datetime, timedelta

from config import settings

APP_ENV = os.environ.get('APP_ENV', 'Dev')
config = getattr(settings, f'{APP_ENV}Config')

uri = config.MONGO_URI

client = MongoClient(uri)

db_name = config.DATABASE_NAME


class MongoDocument(object):
    _id : ObjectId
    created_at : str

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

    @classmethod
    def get_only(cls, **kwargs) -> dict:
        """
        Method to return dict of specified fields.
        REQUIRED attr fields:dict
        User.get_only(email='test@test.com, fields={'_id':False, 'token':True}
        if '_id':False is not specified then the dict will contain _id of a doc.
        """
        fields = {}
        if kwargs.get('fields'):
            fields = {k:1 if v else 0 for k,v in kwargs.pop('fields').items()}
            if (mongo_data := cls.db().find(kwargs, fields)):
                if mongo_data.count() == 1:
                    return mongo_data[0]
                elif mongo_data.count() > 1:
                    raise Exception(
                        f'{cls.__name__}.get() returned more than one element.'\
                        f'It returned {mongo_data.count()}!')
            return None
        raise Exception('fields was not specified')

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
    def filter_only(cls, **kwargs) -> list:
        """same as the get_only() but returns multiple dict objects"""
        fields = {}
        if kwargs.get('fields'):
            fields = {k:1 if v else 0 for k,v in kwargs.pop('fields').items()}
            if (mongo_data := cls.db().find(kwargs, fields)):
                return list(mongo_data)

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
        kwargs['parse_from_date'] = (datetime.now() - timedelta(days=60)).date().isoformat()
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
