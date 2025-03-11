from app import db
from datetime import datetime


class Distribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_station_id = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)
    to_station_id = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
