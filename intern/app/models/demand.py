from app import db
from datetime import datetime


class DemandHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    quantity_requested = db.Column(db.Integer, nullable=False)
