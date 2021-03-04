from bson.objectid import ObjectId
from user.models import User
import uuid
import re
import datetime

class Alert:
    def __init__(self, _id:int, category: str, title: str, description: str,
                is_human_created: bool=False):
        self._id = _id
        self.category = category
        self.title = title
        self.description = description
        self.is_human_created = is_human_created
        self.created_at = datetime.datetime.now().strftime('%d.%m.%Y')

    def generate(self) -> dict:
        """
        Constructs it self in dict/json format to be ready to be insertred in the database
        """
        return {
            "id": self._id,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "is_human_created": self.is_human_created,
            "created_at": self.created_at,
            "active": True
        }

    def format(self, metrics: dict, field: str):
        """
            Inserts values into places { ... } in text of title or description.
            Metrics are used to calculate user`s values
        :param metrics: users metrics from db.
        :param field: field that will be formatting ( ONLY title or description)
        """
        tags = re.findall(r'{.*?}', getattr(self, field))
        tags = [item[1:-1] for item in tags]
        items_func = [getattr(self, item) for item in tags]
        items = []
        for it in items_func:
            items.append(it(metrics)) # Call functions for calculating values { ... }
        self.__dict__[field] = getattr(self, field).format(**dict(zip(tags, items)))


class Tip:
    def __init__(self, _id: int, category: str, title: str, description: str,
                is_human_created: bool=False):
        self._id = _id
        self.category = category
        self.title = title
        self.description = description
        self.is_human_created=is_human_created
        self.created_at = datetime.datetime.now().strftime('%d.%m.%Y')

    def generate(self) -> dict:
        """
        Constructs it self in dict/json format to be ready to be insertred in the database
        """
        return {
            "id": self._id,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "is_human_created": self.is_human_created,
            "created_at": self.created_at,
            "active": True
        }


class MetricAnalyzer(object):

    def analyze(self, user_id):
        function_names = [attr for attr in dir(self) if not attr.startswith('__') and callable(getattr(self, attr)) and attr != 'analyze']
        for name in function_names:
            func = getattr(self, name)
            func_hash = hash(func.__name__)
            alg_type = func.__annotations__.get('return').__name__  # don't proccess the algorithm if the same id is in the database
            if not User.db().find_one({'_id': ObjectId(user_id), f'{alg_type}.id': func_hash, 'active': True}):
                try:
                    if (algorithm := func(func_hash)):
                        User.append_list({'_id': ObjectId(user_id)}, {f'{alg_type}s': algorithm.generate()})
                except Exception as e:
                    with open('log.log', 'a') as f:
                        f.write(f'[ALGORITHM ERROR] - {str(e)} - alg<{func.__name__}>\n')

class MetricNotFoundException(Exception):
    def __init__(self, message:str):
        self.message = message