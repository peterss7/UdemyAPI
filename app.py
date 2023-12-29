import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)

@app.get("/storez") 
def get_stores():
    return { "stores": stores }

@app.get( "/item") 
def get_items():
    return { "items": list(items.values()) }

@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex

    if (
        "name" not in store_data
        or "store_id" not in store_data
    ):
        abort(400, message="Missing data. Store Name and store id are required.")
    
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(404, message="Store already exists")
    
    store = { **store_data, "id": store_id }
    stores[store_id] = store
    return store, 201

@app.post("/item")
def create_item(): 
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Missing data. Item Name, Price and Store ID are required."
        )
    for item in item.values():
        if(
            item_data["name"] == item["name"] 
            and item_data["store_id"] == item["store_id"]
        ):
            abort(404, message="Item already exists")
    
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
    
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError:
        abort(404, message="Item not found")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
