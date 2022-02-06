from flask_restful import Resource
from flask import jsonify, request
from .api_utils import *

class UserStats(Resource):
    def get(self, username):
        forked = request.args.get('forked') == 'true'
        return collect_stats(username, forked)