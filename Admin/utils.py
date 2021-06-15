from config import settings
import os

APP_ENV = os.environ.get('APP_ENV', 'Dev')
config = getattr(settings, f'{APP_ENV}Config')


def build_url(user_chooser_class_route: str):
    return (f'/admin/{user_chooser_class_route}', user_chooser_class_route.replace("-", " "))
