from flask import Flask
from flask_restful import Api

from api.api import *

app = Flask(__name__)
api = Api(app)

api.add_resource(UserStats, '/user_stats/<string:username>')

if __name__ == '__main__':
    app.run(debug=True)