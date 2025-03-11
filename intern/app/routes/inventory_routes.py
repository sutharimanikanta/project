# app/routes/inventory_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.inventory import Inventory
from app.models.station import Station
from app.models.product import Product
from app import db

inventory_blueprint = Blueprint("inventory", __name__, template_folder="../templates")


@inventory_blueprint.route("/")
def list_inventory():
    inventory = Inventory.query.join(Station).join(Product).all()
    return render_template("inventory.html", inventory=inventory)


@inventory_blueprint.route("/add", methods=["GET", "POST"])
def add_inventory():
    stations = Station.query.all()
    products = Product.query.all()
    if request.method == "POST":
        inventory = Inventory(
            station_id=request.form["station_id"],
            product_id=request.form["product_id"],
            quantity=request.form["quantity"],
        )
        db.session.add(inventory)
        db.session.commit()
        return redirect(url_for("inventory.list_inventory"))
    return render_template("add_inventory.html", stations=stations, products=products)


@inventory_blueprint.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_inventory(id):
    inventory = Inventory.query.get_or_404(id)
    stations = Station.query.all()
    products = Product.query.all()
    if request.method == "POST":
        inventory.station_id = request.form["station_id"]
        inventory.product_id = request.form["product_id"]
        inventory.quantity = request.form["quantity"]
        db.session.commit()
        return redirect(url_for("inventory.list_inventory"))
    return render_template(
        "edit_inventory.html", inventory=inventory, stations=stations, products=products
    )


@inventory_blueprint.route("/delete/<int:id>", methods=["POST"])
def delete_inventory(id):
    inventory = Inventory.query.get_or_404(id)
    db.session.delete(inventory)
    db.session.commit()
    return redirect(url_for("inventory.list_inventory"))
