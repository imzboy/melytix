from user import get_g_tokens, query

from requests_oauthlib import OAuth2Session
from oauth2client import client as oauth_client
import httplib2 as lib2
from datetime import datetime, timedelta

import requests

CLIENT_ID = '380470694344-0a4vb8rvio43bje2dmbs5hk7l8ecdglm.apps.googleusercontent.com'
CLIENT_SECRET = 'Z9rH11ECkJ_7ceMmij7JnTWM'


def code_exchange(code: str, uri: str):
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': uri,
        'grant_type': 'authorization_code'
        }

    r = requests.post('https://oauth2.googleapis.com/token', data=data)


    access_token, refresh_token = r.json().get('access_token'), r.json().get('refresh_token')

    if refresh_token:
        return access_token, refresh_token
    else:
        user = query(tokens={'g_access_token':access_token})
        return user['tokens']['g_access_token'], user['tokens']['g_refresh_token']


def get_google_user_data(g_token: str):
    r = requests.get(f'https://www.googleapis.com/oauth2/v2/userinfo?oauth_token={g_token}')

    try:
        if r.json()['verified_email']:
            return r.json()['email'], r.json()['picture']
        return {'Error': 'user email is not verified'}, 403
    except TypeError:
        return {'Error': r.text}, 403


def auth_credentials(token):
    access_token, refresh_token = get_g_tokens(token)

    credentials = oauth_client.GoogleCredentials(
        access_token=access_token,
        refresh_token=refresh_token,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri='https://accounts.google.com/o/oauth2/token',
        token_expiry=(datetime.now() + timedelta(days=10)),
        user_agent='Melytix-user-agent/1.0')
    # authorizing credentials (if token is expired it will refresh it)
    authorized = credentials.authorize(lib2.Http())
    return authorized
