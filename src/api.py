from flask_restful import Resource
from flask import jsonify, request

class Contribution(Resource):
    def get(self):
       return None