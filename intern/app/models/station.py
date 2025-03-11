from app import db


class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    inventory = db.relationship("Inventory", backref="station", lazy=True)
    demand_history = db.relationship("DemandHistory", backref="station", lazy=True)
    distributions_from = db.relationship(
        "Distribution",
        foreign_keys="Distribution.from_station_id",
        backref="from_station",
        lazy=True,
    )
    distributions_to = db.relationship(
        "Distribution",
        foreign_keys="Distribution.to_station_id",
        backref="to_station",
        lazy=True,
    )
