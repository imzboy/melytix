from flask import Flask, request

from flask_restful import Resource, Api

from flask_cors import CORS

import user as User

app = Flask(__name__)
app.secret_key = b"\x92K\x1a\x0e\x04\xcc\x05\xc8\x1c\xc4\x04\x98\xef'\x8e\x1bC\xd6\x18'}:\xc1\x14"

api = Api(app)

cors = CORS(app, resources={r"*": {"origins": ["http://localhost:8080", "https://kraftpy.github.io", "https://kraftpy.github.io/MelytixView"]}})

class HelloView(Resource):
    def get(self):
        return {'Message': 'Hello World!'}


class RegistrationView(Resource):
    """The registration endpoint.
       Takes credentials and creates a new user.
       Credentials : email, password"""

    def post(self):
        email = request.json['email']
        password = request.json['password']
        if not User.get_by_email(email):
            User.register(email, password)
            return {'status': 'success',
                    'email': email}
        else:
            return {'Error': 'User with that email already created'}


class LoginView(Resource):
    def post(self):
        email = request.json['email']
        password = request.json['password']
        verify = User.verify_password(email, password)
        if verify and verify != 404:
            return {'token': User.get_or_create_token(email)}
        elif verify == 404:
            return {'Error': 'user not found'}, 404
        else:
            return {'Error': 'wrong password'}


# URLs declaring
api.add_resource(HelloView, '/', methods=['GET'])
api.add_resource(RegistrationView, '/registration/', methods=['POST'])
api.add_resource(LoginView, '/login/', methods=['POST'])