from Utils import GoogleUtils
from flask_restful import Resource, Api
from Systems.Facebook.FacebookAdsManager import facebook_insights_query
from flask import request, Blueprint
from user.models import User
import datetime
import requests
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

facebook_insg_bp = Blueprint('facebook_insg_api', __name__)
api = Api(facebook_insg_bp)


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
            start_date = user.parse_from_date
            end_date = datetime.datetime.now().date().isoformat()
            #TODO: log the time of the api exec
            facebook_insights = facebook_insights_query(token, start_date, end_date)

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


def facebook_insights_metrics(request):
    user = request.user

    facebook_insights = user.metrics.get('facebook_insights')
    campaign = request.json.get('campaign')
    metric_name = request.json.get('metric')
    dates = facebook_insights.get('dates')
    metric = facebook_insights.get(campaign, {}).get(metric_name)

    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    start_date, end_date = GoogleUtils.find_start_and_end_date(dates, start_date, end_date)
    if metric and dates:
        return {'metric': metric[start_date:end_date], 'dates': dates[start_date:end_date]}, 200


# facebook insights
api.add_resource(FacebookSetAccount, '/insert-fi-account', methods=['POST', 'OPTIONS'])
api.add_resource(FacebookAuthLoginApiView, '/insert-fi-token', methods=['POST', 'OPTIONS'])
