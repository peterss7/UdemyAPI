from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import ItemModel
from schemas import ItemCreateSchema, ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__)

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
        
    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        print(jwt.get("is_admin"))
        if not jwt.get("is_admin"):
            abort(403, message="Admin privilege required") 
        item = ItemModel.query.get_or_404(item_id)
        # db.session.delete(item)
        # db.session.commit()
        return "Message: Item deleted"
            
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(**item_data)
        
        db.session.add(item)
        db.session.commit()

        return item
@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemCreateSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Could not add item to database")
        
        return item