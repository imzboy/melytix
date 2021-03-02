from flask_restful import Api, Resource
from flask import Blueprint, request
from user.models import User
from Utils.decorators import user_auth
from email_validator import validate_email, EmailNotValidError


user_bp = Blueprint('user_api', __name__)
api = Api(user_bp)


class LoginView(Resource):

    def options(self):
        return {},200

    def post(self):
        email = request.json['email']
        password = request.json['password']
        if User.verify_password(email, password):
            return {'token': User.get_or_create_token(email)}
        return {'Error': 'wrong password'}


class LogOutView(Resource):

    def options(self):
        return {}, 200

    @user_auth
    def post(self):
        User.update_one(
            {'auth_token': request.user.token},
            {'auth_token': None})
        return {'Message': 'User logout'}, 200


class RegistrationView(Resource):

    def options(self):
        return {}, 200

    def post(self):
        email: str = request.json.get('email')
        password: str = request.json.get('password')
        plan:str = request.json.get('plan')

        if email and password:
            try:
                validate_email(email)
            except EmailNotValidError as e:
                return {"Message": str(e)}, 400
            else:
                if len(password) >= 8:
                    User.register(email, password, plan)

                    return {'Message': 'success'}, 201

                return {'Message': 'Password length is less than 8'}, 400

        return {'Message': 'Credentials not provided'}, 400


#Login end points
api.add_resource(RegistrationView, '/registration', methods=['POST', 'OPTIONS'])
api.add_resource(LoginView, '/login', methods=['POST', 'OPTIONS'])
api.add_resource(LogOutView, '/logout', methods=['POST', 'OPTIONS'])
