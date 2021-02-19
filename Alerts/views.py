from flask_restful import Resource

from flask import request

import user as User


class RetriveUserAlerts(Resource):

    def options(self):
        return {}, 200

    def post(self):
        if (token := request.json['token']):
            if (user := User.query(auth_token=token)):

                if (alerts := user['Alerts']):

                    return alerts, 200

                return {'Error': 'no alerts has been generated'}, 404

        return {'Error': 'no credentials provided'}, 403



class AlertTipFlipActive(Resource):

    def options(self):
        return {},200

    def post(self):
        if (token := request.json.get('token')):

            if(_id := request.json.get('id')):

                if(type_ := request.json.get('type')):

                    if type_ == 'Tip' or type_ == 'Alert':

                        User.flip_tip_or_alert(token, type_, _id)

                        return {'message': 'success'}, 200

        return {'message':'Bad request. Maybe some of the field was not inputted'}, 400
