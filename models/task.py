from db import db

class TaskModel(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(80)) # max size of name is 80 chars
    desc = db.Column(db.String(80))
    owner = db.Column(db.String(80))
    due_date = db.Column(db.String(80))
    child_tasks = db.Column(db.String(80))
    parent_tasks = db.Column(db.String(80))
    status = db.Column(db.String(80))


    owner_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"id" : self.id, "name" : self.name, "price" : self.price, "store_id" : self.store_id}

    def save_to_db(self): # Used for both create and update operations
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return ItemModel.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1;

    @classmethod
    def find_all(cls):
        return cls.query.all()
