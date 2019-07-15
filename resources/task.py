from flask import Flask, request
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
#import sqlite3

from models.task import TaskModel


class Task(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,
            required=True, help="This field/key is required!")
    parser.add_argument('store_id', type=int,
            required=True, help="Every item needs a store")

    @jwt_required()
    def get(self, name):

        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message" : "Error while retrieving item"}, 500

        if item:
            return item.json(), 200
        else:
            return {'message': 'Requested item not found'}, 404


    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message' : "item with name '{}'already exist".format(name)}, 400

        data = self.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting an item'}, 500

        return item.json(), 201

    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message' : 'Item has been deleted'}

    def put(self, name):

        data = self.parser.parse_args()

        item = ItemModel.find_by_name(name)


        if item is None:
            try:
                item = ItemModel(name, data['price'], data['store_id'])
            except:
                return {'message' : 'Error occured while inserting the item'}, 500
        else:
            try:
                item.price = data['price']
            except:
                return {'message' : 'Error occured while updating the item'}, 500

        item.save_to_db()

        return item.json()



class Task_list(Resource):

    def get(self):

        items = [ x.json() for x in ItemModel.find_all()]

        return {'items' : items}
