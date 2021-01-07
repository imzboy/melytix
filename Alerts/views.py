from flask_restful import Resource, Api

from flask import Flask, request

import user as User


class RetriveUserAlerts(Resource):

    def options(self):
        return {}, 200

    def post(self):
        try:
            token = request.json['token']
            if (user := User.query(auth_token=token)):

                if (alerts := user['Alerts']):

                    active_alerts = []
                    for alert in alerts:
                        if alert['active']:
                            active_alerts.append(alert)

                    return active_alerts, 200
                else:
                    return {'Error': 'no alerts has been generated'}, 404

        except KeyError:
            return {'Error': 'no credentials provided'}, 403
