from flask_restful import Resource
from flask import jsonify, request
from .api_utils import *

class Contribution(Resource):
    def get(self, organization):
        repos = list_repos(organization)
        return sort_contributors(repos)