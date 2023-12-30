import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import stores


blp = Blueprint("stores", __name__)

@blp.route("/stores/<string:store_id>")
class Store(MethodView):
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
            
    def put(self, store_id):
        store_data = request.get_json()
        if (
            "name" not in store_data
            
        ):
            print('bad request')
            abort(400, message="Missing data. Store Name and store id are required.")
        
        try:
            store = stores[store_id]
            store.update(store_data)
            return store
        except KeyError:
            abort(404, message="Store not found")

@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values()) }
    
    def post(self):
        store_data = request.get_json()
        store_id = uuid.uuid4().hex
        if (
            "name" not in store_data
            
        ):
            print('bad request')
            abort(400, message="Missing data. Store Name and store id are required.")
        
        for store in stores.values():
            if store_data["name"] == store["name"] and store:
                abort(404, message="Store already exists")
        
        store = { **store_data, "id": store_id }
        stores[store_id] = store
        return store, 201