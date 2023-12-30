import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import items, stores

blp = Blueprint("items", __name__)

@blp.route("/items/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found")
        
    def delete(self, item_id):
        try:
            del items[item_id]
            return "Item Deleted", 204
        except KeyError:
            abort(404, message="Item not found")
            
    def put(self, item_id):
        item_data = request.get_json()
        if item_data["store_id"] not in stores:
            abort(404, message="Store not found")
        try:
            item = items[item_id]
            item.update(item_data)
            return item
        except KeyError:
            abort(404, message="Item not found")    

@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values()) }
    
    def post(self):
        item_data = request.get_json()
        if item_data["store_id"] not in stores:
            abort(404, message="Store not found")
        item_id = uuid.uuid4().hex
        item = { **item_data, "id": item_id }
        items[item_id] = item
        return item, 201