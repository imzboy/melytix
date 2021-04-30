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
        url = request.json['site_url']

        if request.user.connected_systems.get('site_parser'):
            return {'Error': 'user already connected his site'}

        parse_main_site.delay(str(request.user._id), url)

        request.user.connect_system(
            token=request.token,
            system='site_parser',
            data={'domain': url}
        )

        return {'Message': 'Success'}, 200

api.add_resource(SiteParserView, '/connect-site-parser', methods=['OPTIONS', 'POST'])
