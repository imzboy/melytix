from Alerts.Alert import Alert
from Tips.Tip import Tip
from user import append_list, query_many

from flask_restful import Resource


class MainManualAnalyzeView(Resource):

    def options(self):
        return {}, 200

    def get(self):
        all_users = []
        for user in query_many():
            user.pop('_id', None)
            user.pop('password', None)
            user.pop('salt', None)
            user.pop('auth_token', None)
            user.pop('DashSettings', None)
            user.pop('tokens', None)
            all_users.append(user)

        return {'users': all_users}, 200

    def post(self):
        helper_dict = {
            'Tip': Tip,
            'Alert': Alert
        }
        user_email = self.request.get('email')
        type_ = self.request.get('type')
        category = self.request.get('category')
        description = self.request.get('description')
        title = self.request.get('title')
        is_human_created = True
        item = helper_dict[type_](
            title=title,
            category=category,
            description=description,
            is_human_created=is_human_created
        )
        append_list(
            {'email': user_email},
            {type_: item.generate()})
        return {'message': 'success'}, 200





