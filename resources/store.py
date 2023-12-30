import uuid
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import stores
from schemas import StoreSchema, StoreUpdateSchema


blp = Blueprint("stores", __name__)

@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")
        
    def delete(self, store_id):
        try:
            del stores[store_id]
            return "Store Deleted", 204
        except KeyError:
            abort(404, message="Store not found")
            
    @blp.arguments(StoreUpdateSchema)
    def put(self, store_data, store_id):
        try:
            store = stores[store_id]
            store |= store_data
            return store
        except KeyError:
            abort(404, message="Store not found")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):

        for store in stores.values():
            if store_data["name"] == store["name"] and store:
                abort(404, message="Store already exists")
        
        store_id = uuid.uuid4().hex
        store = { **store_data, "id": store_id }
        stores[store_id] = store
        return store