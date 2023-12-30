import uuid
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import items
from schemas import ItemSchema, ItemUpdateSchema

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
            
    @blp.arguments(ItemUpdateSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not found")

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item_id = uuid.uuid4().hex
        item = { **item_data, "id": item_id }
        items[item_id] = item
        return item, 201