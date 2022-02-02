from flask import Flask
from flask_restful import Resource, Api

from api.api import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Contribution, '/contribution/<string:organization>')

if __name__ == '__main__':
    app.run(debug=True)