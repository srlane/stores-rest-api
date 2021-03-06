import sys
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item with name "{}" already exists.'.format(name)}, 400

        request_data = Item.parser.parse_args()
        item = ItemModel(name, request_data['price'], request_data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500
        
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        else:
            return {'message': 'No item with that name.'}, 404

        return {'message': 'Item deleted'}, 200
        
    def put(self, name):
        request_data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, request_data['price'], request_data['store_id'])
            except:
                return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                item.price = request_data['price']
            except:
                return {"message": "An error occurred updating the item."}, 500
        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
