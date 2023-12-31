from db import db

class ItemTags(db.Model):
    __tablename__ = "item_tags"
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(), db.ForeignKey("items.id"))
    tag_id = db.Column(db.String(), db.ForeignKey("tags.id"))
    
    stores = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="item_tags")