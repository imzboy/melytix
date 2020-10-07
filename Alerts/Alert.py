import uuid

import datetime

class Alert:
    def __init__(self, category: str, title: str, description: str,
                analytics_func):
        self._id = str(uuid.uuid4())
        self.category = category
        self.title = title
        self.description = description
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
            "created_at": self.created_at,
            "active": True
        }
