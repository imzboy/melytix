from config import settings
import os

APP_ENV = os.environ.get('APP_ENV', 'Dev')
config = getattr(settings, f'{APP_ENV}Config')


def build_url(user_chooser_class_route: str):
    url = f'{config.PROTOCOL}://{config.DOMAIN}/admin/{user_chooser_class_route}'
    return f'<br><a href="{url}">{user_chooser_class_route.replace("-", " ")}</a>'
