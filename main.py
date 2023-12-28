from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "Croger",
        "items": [
            {
                "item": "Bleach",
                "price": 2.99
            },
            {
                "item": "Waffles",
                "price": 7
            },
            {
                "item": "Soda Pop",
                "price": 4.99
            }
        ]
    },
    
]

@app.get("/store") #http://127.0.0.1:5001
def get_stores():
    return { "stores": stores }

@app.post("/store")
def create_store():
    data = request.get_json()
    new_store = { "name": data["name"], "items": data["items"] }
    stores.append(new_store)
    return new_store, 201

@app.post("/store/<string:name>/items")
def create_items(name): 
    data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_items = { "item": data["item"], "price": data["price"] } 
            store["items"].append(new_items)
            return new_items, 201
    return { "error_message" "store not found" }, 404

@app.get("/store/<string:name>")
def get_store_by_name(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"ERROR": "store not found"}, 404

@app.get("/store/<string:name>/items")
def get_items_by_store(name):
    for store in stores:
        if store["name"] == name:
            return store["items"]
    return {"ERROR": "Store not found"}, 404
        


    


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
