import datetime
import json
from flask import request, Blueprint
from flask_restful import Resource, Api
from google.ads.google_ads.client import GoogleAdsClient
from google.oauth2.credentials import Credentials
from Systems.GoogleAds.GoogleAds import google_ads_query_metrics
from Utils.decorators import user_auth
from user.models import User
from Utils.GoogleUtils import find_start_and_end_date
from Systems.Google.GoogleAuth import CLIENT_ID, CLIENT_SECRET, code_exchange

google_ads_bp = Blueprint('google_ads_bp', __name__)
api = Api(google_ads_bp)


SCOPE = 'https://www.googleapis.com/auth/adwords'
DEVELOPER_TOKEN = 'vRm9-k8iVkRprjZw9fkc7w' # TODO: get from main account


class GoogleAdsAuthLoginApiView(Resource):
    def options(self):
        return {}, 200

    @user_auth
    def post(self):
        code = request.json['code']
        token = request.json['token']

        uri = 'http://localhost:8080'  # TODO поменять на 'melytix.tk'

        access_token, refresh_token = code_exchange(code, uri)

        if not refresh_token:
            return {'error': 'No refresh token got. The user needs to revoke access'}, 404

        User.insert_tokens(token, access_token, refresh_token)

        credentials = Credentials(access_token, refresh_token, scopes=SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        customer_client = GoogleAdsClient(credentials, DEVELOPER_TOKEN)
        customer_service = customer_client.get_service("CustomerService", version="v6")
        accessible_customers = customer_service.list_accessible_customers()

        customers = []  # All accounts with level == 0
        for accessible_customer in accessible_customers.resource_names:
            customer = customer_service.get_customer(accessible_customer)
            customers.append({'name': customer.descriptive_name, 'id': customer.id, 'accounts': []})

        # retrieve accounts with level == 1, for each account with level == 0
        google_ads_service = customer_client.get_service("GoogleAdsService", version="v6")
        for index, customer in enumerate(customers):
            query = """
                        SELECT
                          customer_client.descriptive_name,
                          customer_client.id,
                          customer_client.level
                        FROM customer_client
                        WHERE customer_client.level = 1"""
            response = google_ads_service.search(str(customer.get('id')), query)
            for row in response:
                customers[index]['accounts'].append({'name': row.customer_client.descriptive_name,
                                                     'id': row.customer_client.id})

        return {'customers': customers}, 200


class GoogleAdsSetAccount(Resource):
    def options(self):
        return {}, 200

    @user_auth
    def post(self):

        token = request.json['token']
        customer_id = request.json['customer_id']
        customer_name = request.json['customer_name']
        account_id = request.json['account_id']
        account_name = request.json['account_name']

        scopes = [SCOPE]

        start_date = User.parse_from_date
        end_date = datetime.datetime.now().date().isoformat()
        googleads_metrics = google_ads_query_metrics(token, start_date, end_date)

        with open(f'users_metrics/{request.token}/metrics.json', 'r+') as f:
            all_metrics = json.loads(f.read())
            all_metrics['google_ads'] = googleads_metrics
            f.write(json.dumps(all_metrics))

        # User.insert_data_in_db(token, 'google_ads', googleads_metrics)

        User.connect_system(token, 'google_ads', {'customer_id': customer_id, 'customer_name': customer_name,
                                                  'account_id': account_id, 'account_name': account_name,
                                                  'scopes': scopes})

        return {'Message': 'Nice'}, 200


def google_ads_metrics(request):
    if not request.user.connected_systems.get('google_ads'):
        return {'Error': 'Google Ads not connected yet'}, 403

    google_ads_dict_data = request.user.metrics.get('google_ads')
    metric_name = request.json.get('metric')
    metric = google_ads_dict_data.get(metric_name)
    dates = google_ads_dict_data.get('sc_dates')

    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    start_date, end_date = find_start_and_end_date(dates, start_date, end_date)

    if metric and dates:
        return {'metric': metric[start_date:end_date], 'dates': dates[start_date:end_date]}, 200


api.add_resource(GoogleAdsAuthLoginApiView, '/googleads-insert-tokens', methods=['POST', 'OPTIONS'])
api.add_resource(GoogleAdsSetAccount, '/googleads-set-customers', methods=['POST', 'OPTIONS'])
