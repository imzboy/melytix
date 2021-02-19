from user import query
from flask import request

def user_auth(func):
    def wrapper(*args, **kwargs):
        if(token := request.json.get('token')):
            if (user := query(auth_token=token)):
                request.user = user
                return func(args, kwargs)

            return {'Error': 'Wrong auth token'}, 403

        return {'Error': 'no credentials provided'}
    return wrapper
