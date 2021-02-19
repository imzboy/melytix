from flask_restful import Resource
from Systems.Facebook.FacebookAdsManager import facebook_insights_query
from flask import request
from user import User
import datetime
import requests
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount


class FacebookSetAccount(Resource):
    def options(self):
        return {}, 200

    def post(self):

        token = request.json['token']
        account_id = request.json['id']
        name = request.json['name']

        if (user := User.get(auth_token=token)):

            User.connect_system(token, 'facebook_insights', {'account_id': account_id, 'name': name})

            # request for insights for last 3 weeks
            three_weeks_ago = (datetime.datetime.now() - datetime.timedelta(weeks=3))
            today = datetime.datetime.now()
            facebook_insights = facebook_insights_query(token, three_weeks_ago, today)

            # add insights to DB (Create fields)
            User.insert_data_in_db(token, 'facebook_insights', facebook_insights)

            return {'Message': 'Success'}, 200

        return {'Error': 'Wrong auth token'}, 403


class FacebookAuthLoginApiView(Resource):
    def options(self):
        return {}, 200

    def post(self):
        access_token = request.json['access_token']
        token = request.json['token']

        if User.get(auth_token=token):

            User.f_insert_tokens(token, access_token)
            r = requests.get(f'https://graph.facebook.com/v9.0/me/adaccounts?access_token={access_token}')
            FacebookAdsApi.init(access_token=access_token)
            data = r.json().get('data')

            if data:
                accounts = []
                for id in data:
                    my_account = AdAccount(id.get('id'))
                    account_data = dict(my_account.api_get(fields=[AdAccount.Field.name]))
                    temp_account = {}
                    for key, value in account_data.items():
                        temp_account[key] = value if isinstance(value, str) else value.decode('utf-8')
                    accounts.append(temp_account)
                return accounts, 200

            return {'Message': 'User has no accounts'}, 200

        return {'Error': 'Wrong auth token'}, 403


class RetrieveFacebookMetricsFromBD(Resource):
    def options(self):
        return {}, 200

    def post(self):
        if (user := User.get(auth_token=request.json['token'])):

            result = {}
            facebook_insights = user.metrics.get('facebook_insights')
            for campaign, metrics in facebook_insights.items():
                temp = {}
                for metric_name, list_value in metrics.items():
                    temp.update({metric_name: list_value[-7:]})
                result.update({campaign: temp})

            return result, 200

        return {'Error': 'Wrong auth token'}, 403
