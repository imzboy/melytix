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

                    active_tips = []
                    for alert in tips:
                        if alert['active']:
                            active_tips.append(alert)

                    return active_tips, 200
                else:
                    return {'Error': 'no tips has been generated'}, 404

        return {'Error': 'no credentials provided'}, 403