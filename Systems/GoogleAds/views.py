import json

import requests
from flask import request, Blueprint
from flask_restful import Resource, Api
from google.ads.google_ads.client import GoogleAdsClient
from google.oauth2.credentials import Credentials
from google.protobuf.json_format import MessageToJson

from Utils.decorators import user_auth
from user.models import User

google_ads_bp = Blueprint('google_ads_bp', __name__)
api = Api(google_ads_bp)

CLIENT_ID = '103210160069-f861hj9s588bntthl14i14ctvpjhr4ca.apps.googleusercontent.com'
CLIENT_SECRET = 'ssWM9CUWBnaDGyL92raQEOyp'
SCOPE = 'https://www.googleapis.com/auth/adwords'
REDIRECT_URI = 'http://127.0.0.1:5000/oauth2callback'
DEVELOPER_TOKEN = 'vRm9-k8iVkRprjZw9fkc7w'


class GetCustomers(Resource):
    def options(self):
        return {}, 200

    @user_auth
    def post(self):
        code = request.json['code']
        token = request.json['token']

        auth_data = {'code': code,
                     'client_id': CLIENT_ID,
                     'client_secret': CLIENT_SECRET,
                     'redirect_uri': REDIRECT_URI,
                     'grant_type': 'authorization_code'}

        auth_request = requests.post('https://accounts.google.com/o/oauth2/token', data=auth_data)
        access_token = auth_request.json().get('access_token')
        refresh_token = auth_request.json().get('refresh_token')

        if not refresh_token:
            return {'error': 'No refresh token got. The user needs to revoke access'}, 404

        User.insert_tokens(token, access_token, refresh_token)

        credentials = Credentials(access_token, refresh_token, scopes=SCOPE, client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET)
        client = GoogleAdsClient(credentials, DEVELOPER_TOKEN)
        service = client.get_service("CustomerService", version="v6")
        accessible_customers = service.list_accessible_customers()

        customers = []  # All accounts with level == 0
        for accessible_customer in accessible_customers.resource_names:
            customer = service.get_customer(accessible_customer)
            customers.append({'name': customer.descriptive_name, 'id': customer.id, 'accounts': []})

        # retrieve accounts with level == 1, for each account with level == 0
        google_ads_service = client.get_service("GoogleAdsService", version="v6")
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
                json_str = MessageToJson(row)
                response_dict = json.loads(json_str)
                account_name = response_dict.get('customerClient').get('descriptiveName')
                id = response_dict.get('customerClient').get('id')
                customers[index]['accounts'].append({'name': account_name, 'id': id})

        return customers, 200




api.add_resource(GetCustomers, '/googleads-get-customers', methods=['POST', 'OPTIONS'])
