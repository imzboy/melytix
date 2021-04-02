from flask_restful import Api, Resource
from flask import Blueprint, request
from user.models import User
from Utils.decorators import user_auth
from email_validator import validate_email, EmailNotValidError
import datetime


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
        language:str = request.json.get('language')
        if email and password:
            try:
                validate_email(email)
            except EmailNotValidError as e:
                return {"Message": str(e)}, 400
            else:
                if not User.get(email=email):
                    if len(password) >= 8:
                        User.register(email, password, language, plan)

                        return {'Message': 'success'}, 201

                    return {'Message': 'Password length is less than 8'}, 400
                return {'Message': 'User with this email already exists'}, 400
        return {'Message': 'Credentials not provided'}, 400


class DeleteAccount(Resource):

    def options(self):
        return {},200

    @user_auth
    def post(self):
        delete_date = (datetime.datetime.today() + datetime.timedelta(days=14)).date().isoformat()
        if User.update_one(filter={'auth_token': request.token}, update={'delete_date': delete_date}):
            return {'Message': 'success'}
        return {'Message': 'Error, try again'}


class ChangeCreds(Resource):

    def options(self):
        return {},200

    @user_auth
    def post(self):

        if email := request.json.get('email'):
            if email == request.user.email:
                return {'Message': 'Error, this email is already the same as the old one'}
            User.update_one(filter={'auth_token': request.token}, update={'email': email})

        if language := request.json.get('lang'):
            if language == request.user.language:
                return {'Message': 'Error, this language is already the same as the old one'}
            User.update_one(filter={'auth_token': request.token}, update={'language': language})

        if old_pass := request.json.get('old_pass'):
            base_pass = request.user.password

            if old_pass == base_pass:
                new_pass = request.json.get('new_pass')
                if new_pass == base_pass:
                    return {'Message': 'Error, this password is already the same as the old one'}
                User.update_one(filter={'auth_token': request.token}, update={'password': new_pass})
            else:
                return {'Message': 'Error, invalid password'}
        return {'Message': 'success'}


#Login end points
api.add_resource(RegistrationView, '/registration', methods=['POST', 'OPTIONS'])
api.add_resource(LoginView, '/login', methods=['POST', 'OPTIONS'])
api.add_resource(LogOutView, '/logout', methods=['POST', 'OPTIONS'])
api.add_resource(DeleteAccount, '/delete', methods=['POST', 'OPTIONS'])
api.add_resource(ChangeCreds, '/change-creds', methods=['POST', 'OPTIONS'])
