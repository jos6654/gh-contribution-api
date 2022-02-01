from flask import Flask
from flask_restful import Resource, Api

from api import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Contribution, '/contribution')

if __name__ == '__main__':
    print("Starting flask")
    app.run(debug=True)