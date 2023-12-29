import uuid
from flask import Flask, request
from flask_smorest import abort
from UdemyAPI.db import stores, items

app = Flask(__name__)

@app.get("/store") 
def get_stores():
    return { "stores": stores }

@app.get( "/item") 
def get_items():
    return { "items": list(items.values()) }

@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = { **store_data, "id": store_id }
    stores[store_id] = store
    return store, 201

@app.post("/item")
def create_item(store_id): 
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")
    item_id = uuid.uuid4().hex
    item = { **item_data, "id": item_id }
    items[item_id] = item
    return item, 201

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")

@app.get("/store/<string:item_id>/")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found")
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
