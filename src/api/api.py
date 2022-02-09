from flask_restful import Resource
from flask import request
from .api_utils import *

class UserStats(Resource):
    def get(self, username):
        forked = request.args.get('forked') == 'true' or request.args.get('forked') == None
        return collect_stats(username, forked)