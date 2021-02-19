from Utils.decorators import user_auth
from flask_restful import Resource, Api

from flask import Flask, request

import user as User


class RetriveUserTips(Resource):

    def options(self):
        return {}, 200

    @user_auth
    def post(self):

        if (tips := request.user.Tips):

            return tips, 200

        return {'Error': 'no tips has been generated'}, 404
