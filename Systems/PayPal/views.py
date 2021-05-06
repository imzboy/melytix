from flask import request, Blueprint
from flask_restful import Api, Resource
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCaptureRequest

from user.models import User
from Utils.decorators import user_auth


CLIENT_ID = 'Acc6GBIJYIeyEs2bJ9BNtlQdsPJRDaeKNvr6gN91iRuRXdRd9dfUE4KacvlWethIpnEy2Iq-EUdAqcTb'
CLIENT_SECRET = 'EFIdl4ElBmd0V1S_f9BwN9xmmazBsehUoggkggxyBa943ahjYNTLCLT4tAB6bZXa0EPS15w03Yl8Xzxf'

paypal_bp = Blueprint('paypal_api', __name__)
api = Api(paypal_bp)


class CreateOrder(Resource):

    def options(self):
        return {}, 200

    @user_auth
    def post(self):
        environment = SandboxEnvironment(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        client = PayPalHttpClient(environment)
        req = OrdersCreateRequest()
        req.prefer('return=representation')
        req.request_body(
            {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": "USD",
                            "value": "30.00"
                        }
                    }
                ]
            }
        )
        try:
            # Call API with your client and get a response for your call
            response = client.execute(req)
        except IOError:

            return {'Error': 'Something went wrong'}, 400

        return {'payment_id': response.result.id}


class CaptureOrder(Resource):

    def options(self):
        return {}, 200

    @user_auth
    def post(self):
        req = OrdersCaptureRequest(request.get('payment_id'))

        try:
            # Call API with your client and get a response for your call
            environment = SandboxEnvironment(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
            client = PayPalHttpClient(environment)
            client.execute(req)

        except IOError:
            return {'Error': 'Something went wrong'}, 400

        User.update_one(filter={'auth_token': request.token}, update={'plan': 'premium'})

        return {'Message': 'Success'}, 200


api.add_resource(CreateOrder, '/payment', methods=['POST', 'OPTIONS'])
api.add_resource(CaptureOrder, '/execute', methods=['POST', 'OPTIONS'])
