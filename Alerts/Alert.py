

class Alert:
    def __init__(self, _id: str, category: str, title: str, description: str, 
                analytics_func: function):
        self._id = _id
        self.category = category
        self.title = title
        self.description = description
        self.analytics_func = analytics_func

    def generate(self) -> dict:
        """
        Constructs it self in dict format to be ready to be insertred in the database
        """
        return {
            "id": self.id,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "active": True
        }
