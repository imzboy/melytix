from pymongo.collection import Collection
from Utils.utils import NestedDict, all_dict_paths
import os
from pymongo import MongoClient
from pymongo.results import InsertOneResult
from bson import ObjectId
from datetime import datetime, timedelta

from config import settings

APP_ENV = os.environ.get('APP_ENV', 'Dev')
config = getattr(settings, f'{APP_ENV}Config')

uri = config.MONGODB_URI

client = MongoClient(uri)

db_name = config.DATABASE_NAME


class MetricsUserManager(object):


    def __init__(self, user_id : str) -> None:
        self.user_id : ObjectId = ObjectId(user_id)


    def db(self, system_name: str, **kwargs) -> Collection:
        """
        kwargs table type stands for totals or filtered
        """

        if kwargs.get('table_type'):
            return client.__getattr__(db_name).__getattr__(f'{system_name}_{kwargs["table_type"]}')

        return client.__getattr__(db_name).__getattr__(f'{system_name}')


    def initial_insert(self, metrics : dict, dates: list, system_name : str, **kwargs):
        db = self.db(system_name, **kwargs)
        paths = all_dict_paths(metrics)
        ordered_values = zip(*[item[1] for item in paths])

        result = NestedDict()
        for values, date in zip(ordered_values, dates):
            date = datetime.strptime(date, '%Y-%m-%d')
            for path, _ in paths:
                for value in values:
                    exec(f'result{str(path).replace(", ", "][")}=value')

            db.insert_one({'date': date, 'user_id': self.user_id, **result})


    def daily_update(self, metrics: dict, date : str, system_name: str, **kwargs):
        db = self.db(system_name, **kwargs)

        date = datetime.strptime(date, '%Y-%m-%d')
        all_paths = all_dict_paths(metrics)

        result = NestedDict()
        for i, path, value in enumerate(all_paths):
            exec(f'result{str(path).replace(", ", "][")}=value[0]')

        db.insert_one({'date': date, 'user_id': self.user_id, **result})


    def get_by_range(self, system_name: str, start_date: str, end_date: str, **kwargs) -> dict:
        db = self.db(system_name, **kwargs)
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        metrics = db.find({'user_id': self.user_id, 'date': {'$lt': end_date, '$gte': start_date}})

        if not metrics:
            return

        dates = []
        all_paths = []
        for metric_slice in metrics:
            metric_slice.pop('_id')
            dates.append(str(metric_slice.pop('date').date()))
            metric_slice.pop('user_id')
            all_paths.append(all_dict_paths(metric_slice))

        paths, values = [], []

        for dict_paths in all_paths:
            for path, value in dict_paths:
                if len(paths):
                    if path in paths:
                        i = paths.index(path)
                        values[i].append(value)
                    else:
                        paths.append(path)
                        values.append([value])

                else:
                    paths.append(path)
                    values.append([value])

        end_paths = zip(paths, values)

        ret = NestedDict()

        for path, value in end_paths:
            exec(f'ret{str(path).replace(", ", "][")}=value')

        ret['dates'] = dates

        return ret


    def last_date(self, system_name: str, **kwargs) -> dict:
        '''searches trough the db to find the entry with closest date to today'''

        db = self.db(system_name, **kwargs)

        metrics : dict = db.find({'user_id': self.user_id}).sort('date', -1).limit(1)
        if metrics:
            metrics = metrics[0]

            metrics['dates'] = str(metrics['date'].date())

            metrics.pop('date')
            metrics.pop('user_id')
            metrics.pop('_id')

            return metrics
        return None


    def week(self, system_name: str, **kwargs) -> dict:
        today = datetime.now().date()
        week_before = (today - timedelta(days=7)).isoformat()

        return self.get_by_range(system_name, week_before, today.isoformat(), **kwargs)


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
            elif mongo_data.count() > 1:
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
    def delete(cls, **kwargs):
        cls.db().delete_one(kwargs)

    @classmethod
    def update_one(cls, filter, update):
        """
        Finds and updates user data.
        Function does not insert a new document when no match is found.
            Parameters:
                filter (dict): parameters for user search
                update (dict): updated user`s data
        """
        return cls.db().find_one_and_update(
            filter,
            {'$set': update},
            upsert=False
        )


    def __getattribute__(self, name: str):
        if name in ['data', 'is_active', 'is_authenticated', 'is_anonymous', 'get_id', 'metrics']:  #TODO: rework
            return object.__getattribute__(self, name)

        attr = self.data.get(name, {}) #TODO: bad...
        return attr

    def __setattr__(self, name: str, value):

        if name == 'data':
            object.__setattr__(self, name, value)
        else:
            self.data.update({name: value})

    @property
    def dict(self):
        return self.data
