import os

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from resources.user import UserRegister
from resources.task import Task, Task_list

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db') # data.db resides at root directory of project
#app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = 'sangram'
api = Api(app)

jwt = JWT(app, authenticate, identity) # creates a new endpoint /auth

api.add_resource(Task, '/Task/<string:name>')
api.add_resource(Task_list, '/Task_list')
api.add_resource(UserRegister, '/User')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
