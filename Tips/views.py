from flask_restful import Resource, Api

from flask import Flask, request

import user as User


class RetriveUserTips(Resource):

    def options(self):
        return {}, 200

    def post(self):
        if (token := request.json['token']):
            if (user := User.query(auth_token=token)):

                if (tips := user.get('Tips')):

                    return tips, 200

                return {'Error': 'no tips has been generated'}, 404

        return {'Error': 'no credentials provided'}, 403
