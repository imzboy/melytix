from user.models import User
from flask import request


def user_auth(func):

    def wrapper(*args, **kwargs):

        if(token := request.json.get('token')):
            if (user := User.get(auth_token=token)):
                request.user = user
                request.token = token
                return func(*args, **kwargs)

            return {'Error': 'Wrong auth token'}, 403

        return {'Error': 'no credentials provided'}

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper
