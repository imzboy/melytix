import uuid
import re
import datetime


class Alert:
    def __init__(self, _id: str, category: str, title: str, description: str,
                is_human_created: bool=False, analytics_func=None):
        self._id = _id
        self.category = category
        self.title = title
        self.description = description
        self.is_human_created = is_human_created
        self.analytics_func = analytics_func
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


