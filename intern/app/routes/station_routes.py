from flask import Blueprint, render_template, request, redirect, url_for
from app.models.station import Station
from app import db

station_blueprint = Blueprint("station", __name__, template_folder="../templates")


@station_blueprint.route("/")
def list_stations():
    stations = Station.query.all()
    return render_template("stations.html", stations=stations)


@station_blueprint.route("/add", methods=["GET", "POST"])
def add_station():
    if request.method == "POST":
        station = Station(
            name=request.form["name"],
            location=request.form["location"],
            description=request.form["description"],
        )
        db.session.add(station)
        db.session.commit()
        return redirect(url_for("station.list_stations"))
    return render_template("add_station.html")


@station_blueprint.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_station(id):
    station = Station.query.get_or_404(id)

    if request.method == "POST":
        station.name = request.form["name"]
        station.location = request.form["location"]
        station.description = request.form["description"]
        db.session.commit()
        return redirect(url_for("station.list_stations"))

    return render_template("edit_station.html", station=station)


@station_blueprint.route("/delete/<int:id>", methods=["POST"])
def delete_station(id):
    station = Station.query.get_or_404(id)
    db.session.delete(station)
    db.session.commit()
    return redirect(url_for("station.list_stations"))
