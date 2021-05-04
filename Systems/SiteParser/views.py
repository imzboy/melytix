from user.models import User
from flask import request, Blueprint
from flask_restful import Resource, Api

from Utils.decorators import user_auth

parser_bp = Blueprint('parser_api', __name__)
api = Api(parser_bp)

from tasks.tasks import parse_main_site

class SiteParserView(Resource):

    def options(self):
        return {},200

    @user_auth
    def post(self):

        '''parser logic'''
        url = request.json.get('site_url')
        if url:

            if request.user.connected_systems.get('site_parser'):
                return {'Error': 'user already connected his site'}

            # parse_main_site.delay(str(request.user._id), url)

            User.connect_system(
                token=request.token,
                system='site_parser',
                data={'domain': url}
            )

            return {'Message': 'Success'}, 200
        return {'Error': 'site_url was not provided'}


class SiteParserUrls(Resource):

    def options(self):
        return {}, 200


    def get(self):
        users = User.filter()
        sites = []
        for user in users:
            if user.connected_systems.get('site_parser'):
                sites.append((user.email, user.connected_systems.get('site_parser').get('domain')))

        return {'sites':sites}, 200



api.add_resource(SiteParserView, '/connect-site-parser', methods=['OPTIONS', 'POST'])
api.add_resource(SiteParserUrls, '/site-parser-urls', methods=['OPTIONS', 'GET'])