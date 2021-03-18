from flask_restful import Resource, Api

from flask import request, Blueprint

from user.models import User
from Utils.decorators import user_auth

algorithms_bp = Blueprint('algorithms_api', __name__)
api = Api(algorithms_bp)


class RetriveUserAlerts(Resource):

    def options(self):
        return {}, 200

    @user_auth
    def post(self):

        if (alerts := request.user.Alerts):
            lang = request.user.language
            for alert in alerts:
                alert_text = alert.pop(lang)
                alert.pop('ru' if lang == 'en' else 'en')
                alert.update(alert_text)
            # alerts = list(filter(lambda x: x.get('active'), alerts))

            return alerts, 200

        return {'Error': 'no alerts has been generated'}, 404



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


class RetriveUserTips(Resource):

    def options(self):
        return {}, 200

    @user_auth
    def post(self):

        if (tips := request.user.Tips):
            lang = request.user.language
            for tip in tips:
                tip_text = tip.pop(lang)
                tip.pop('ru' if lang == 'en' else 'en')
                tip.update(tip_text)
            # tips = list(filter(lambda x: x.get('active'), tips))

            return tips, 200

        return {'Error': 'no tips has been generated'}, 404


#alerts and tips
api.add_resource(RetriveUserAlerts, '/get-alerts', methods=['POST', 'OPTIONS'])
api.add_resource(RetriveUserTips, '/get-tips', methods=['POST', 'OPTIONS'])
api.add_resource(AlertTipFlipActive, '/flip', methods=['POST', 'OPTIONS'])
