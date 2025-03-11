# app/routes/distribution_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.distribution import Distribution
from app.models.station import Station
from app.models.product import Product
from app import db

distribution_blueprint = Blueprint(
    "distribution", __name__, template_folder="../templates"
)


@distribution_blueprint.route("/")
def list_distributions():
    distributions = (
        Distribution.query.join(Station, Distribution.from_station).join(Product).all()
    )
    return render_template("distributions.html", distributions=distributions)


@distribution_blueprint.route("/add", methods=["GET", "POST"])
def add_distribution():
    stations = Station.query.all()
    products = Product.query.all()
    if request.method == "POST":
        distribution = Distribution(
            from_station_id=request.form["from_station_id"],
            to_station_id=request.form["to_station_id"],
            product_id=request.form["product_id"],
            quantity=request.form["quantity"],
        )
        db.session.add(distribution)
        db.session.commit()
        return redirect(url_for("distribution.list_distributions"))
    return render_template(
        "add_distribution.html", stations=stations, products=products
    )


@distribution_blueprint.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_distribution(id):
    distribution = Distribution.query.get_or_404(id)
    stations = Station.query.all()
    products = Product.query.all()
    if request.method == "POST":
        distribution.from_station_id = request.form["from_station_id"]
        distribution.to_station_id = request.form["to_station_id"]
        distribution.product_id = request.form["product_id"]
        distribution.quantity = request.form["quantity"]
        db.session.commit()
        return redirect(url_for("distribution.list_distributions"))
    return render_template(
        "edit_distribution.html",
        distribution=distribution,
        stations=stations,
        products=products,
    )


@distribution_blueprint.route("/delete/<int:id>", methods=["POST"])
def delete_distribution(id):
    distribution = Distribution.query.get_or_404(id)
    db.session.delete(distribution)
    db.session.commit()
    return redirect(url_for("distribution.list_distributions"))
