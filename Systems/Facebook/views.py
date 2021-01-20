from flask_restful import Resource
from Systems.Facebook.FacebookAdsManager import facebook_insights_query
from flask import request
import user as User
import datetime
import requests
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

from authlib.integrations.flask_client import OAuth

oauth = OAuth()


class FacebookGetAccounts(Resource):
    def options(self):
        return {}, 200

    def get(self):
        if (user := User.query(auth_token=request.json['token'])):

            access_token = user.get('tokens').get('f_access_token')
            r = requests.get(f'https://graph.facebook.com/v9.0/me/adaccounts?access_token={access_token}')
            FacebookAdsApi.init(access_token=access_token)
            accounts = []
            for id in r.json().get('data'):
                my_account = AdAccount(id.get('id'))
                accounts.append(dict(my_account.api_get(fields=[AdAccount.Field.name])))

            return accounts, 200
        else:
            return {'Error': 'Wrong auth token'}, 403



class FacebookSetAccount(Resource):
    def options(self):
        return {}, 200

    def post(self):
        if (user := User.query(auth_token=request.json['token'])):

            account_id = request.json['id']
            User.find_and_update(
                filter={'auth_token': request.json['token']},
                update={
                    'connected_system.facebook_insights.account_id': account_id
                }
            )

            return {'Message': 'Success'}, 200

        return {'Error': 'Wrong auth token'}, 403


class FacebookAuthLoginApiView(Resource):
    def options(self):
        return {}, 200

    def post(self):
        code = request.json['code']
        token = request.json['token']
        if (user := User.query(auth_token=token)):
            oauth.register(
                name='facebook',
                client_id='2892950844365145',
                client_secret='a128271472171c63862424f8d6cd2b6d',
                access_token_url='https://graph.facebook.com/oauth/access_token',
                api_base_url='https://www.facebook.com/',
                client_kwargs={'scope': 'ads_read'}
            )
            response = oauth.facebook.authorize_access_token(code=code)
            access_token = response.get('access_token')
            User.f_insert_tokens(token, access_token)

            # request for insights for last 3 weeks
            three_weeks_ago = (datetime.datetime.now() - datetime.timedelta(weeks=3))
            today = datetime.datetime.now()
            facebook_insights = facebook_insights_query(token, three_weeks_ago, today)

            # add insights to DB (Create fields)
            User.find_and_update(
                filter={'auth_token': request.json['token']},
                update={
                    'metrics.facebook_insights': facebook_insights
                }
            )
            return {'Message': 'Success'}, 200

        return {'Error': 'Wrong auth token'}, 403


class RetrieveFacebookMetricsFromBD(Resource):
    def options(self):
        return {}, 200

    def post(self):
        if (user := User.query(auth_token=request.json['token'])):

            result = {}
            facebook_insights = user.get('connected_system').get('facebook_insights')
            for campaign, metrics in facebook_insights.items():
                temp = {}
                for metric_name, list_value in metrics.items():
                    temp.update({metric_name: list_value[-7:]})
                result.update({campaign: temp})

            return result, 200

        return {'Error': 'Wrong auth token'}, 403
