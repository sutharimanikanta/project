# app/routes/demand_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.demand import DemandHistory
from app.models.station import Station
from app.models.product import Product
from app import db

demand_blueprint = Blueprint("demand", __name__, template_folder="../templates")


@demand_blueprint.route("/")
def list_demand():
    demands = DemandHistory.query.join(Station).join(Product).all()
    return render_template("demand.html", demands=demands)


@demand_blueprint.route("/add", methods=["GET", "POST"])
def add_demand():
    stations = Station.query.all()
    products = Product.query.all()
    if request.method == "POST":
        demand = DemandHistory(
            station_id=request.form["station_id"],
            product_id=request.form["product_id"],
            quantity_requested=request.form["quantity"],
        )
        db.session.add(demand)
        db.session.commit()
        return redirect(url_for("demand.list_demand"))
    return render_template("add_demand.html", stations=stations, products=products)


@demand_blueprint.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_demand(id):
    demand = DemandHistory.query.get_or_404(id)
    stations = Station.query.all()
    products = Product.query.all()
    if request.method == "POST":
        demand.station_id = request.form["station_id"]
        demand.product_id = request.form["product_id"]
        demand.quantity_requested = request.form["quantity"]
        db.session.commit()
        return redirect(url_for("demand.list_demand"))
    return render_template(
        "edit_demand.html", demand=demand, stations=stations, products=products
    )


@demand_blueprint.route("/delete/<int:id>", methods=["POST"])
def delete_demand(id):
    demand = DemandHistory.query.get_or_404(id)
    db.session.delete(demand)
    db.session.commit()
    return redirect(url_for("demand.list_demand"))
