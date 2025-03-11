from flask import Blueprint, render_template, request, redirect, url_for
from app.models.product import Product
from app import db

product_blueprint = Blueprint("product", __name__, template_folder="../templates")


@product_blueprint.route("/")
def list_products():
    products = Product.query.all()
    return render_template("products.html", products=products)


@product_blueprint.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        product = Product(
            name=request.form["name"], description=request.form["description"]
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("product.list_products"))
    return render_template("add_product.html")


@product_blueprint.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == "POST":
        product.name = request.form["name"]
        product.description = request.form["description"]
        db.session.commit()
        return redirect(url_for("product.list_products"))
    return render_template("edit_product.html", product=product)


@product_blueprint.route("/delete/<int:id>", methods=["POST"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("product.list_products"))
