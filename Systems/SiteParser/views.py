from Systems.SiteParser.parser import SiteParser
from flask import request, Blueprint
from flask_restful import Resource, Api

from Utils.decorators import user_auth

parser_bp = Blueprint('parser_api', __name__)
api = Api(parser_bp)

class SiteParserView(Resource):

    def options(self):
        return {},200

    @user_auth
    def post(self):

        '''parser logic'''
        url = request.json['site_url']

        result = SiteParser(url).parse()

        return {'result': result},200

api.add_resource(SiteParserView, '/url', methods=['OPTIONS', 'POST'])
