from app import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    inventory = db.relationship("Inventory", backref="product", lazy=True)
    demand_history = db.relationship("DemandHistory", backref="product", lazy=True)
    distributions = db.relationship("Distribution", backref="product", lazy=True)
