from user import get_g_tokens
import requests

CLIENT_ID = '380470694344-0a4vb8rvio43bje2dmbs5hk7l8ecdglm.apps.googleusercontent.com'
CLIENT_SECRET = 'Z9rH11ECkJ_7ceMmij7JnTWM'


def code_exchange(code: str):
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': ['https://kraftpy.github.io',
                         'http://localhost:8080',
                         'http://127.0.0.1:8080'],
        'grant_type': 'authorization_code'
        }

    r = requests.post('https://oauth2.googleapis.com/token', data=data)

    if r.status_code == 200:
        return r.text['access_token'], r.text['refresh_token']

    print(r.text)
    return {'Error': 'google unreachable'}, 403



def get_google_user_data(g_token: str):
    data = {
        'oauth_token': g_token
    }
    r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', data=data)

    if r.status_code == 200:

        if r.text['verified_email']:

            return r.text['email'], r.text['picture']

        return {'Error': 'user email is not verified'}, 403

    return {'Error': 'google unreachable'}, 403

def auth_credentials(token):
    access_token, refresh_token = User.get_g_tokens(token)

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
    # return authorized
