import uuid

import datetime


class Tip:
    def __init__(self, _id,  category: str, title: str, description: str,
                is_human_created: bool=False, analytics_func=None):
        self._id = _id
        self.category = category
        self.title = title
        self.description = description
        self.analytics_func = analytics_func
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
