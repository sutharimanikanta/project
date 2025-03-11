from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask import render_template

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, template_folder="app/templates")
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.station_routes import station_blueprint
    from app.routes.product_routes import product_blueprint
    from app.routes.inventory_routes import inventory_blueprint
    from app.routes.demand_routes import demand_blueprint
    from app.routes.distribution_routes import distribution_blueprint

    app.register_blueprint(station_blueprint, url_prefix="/stations")
    app.register_blueprint(product_blueprint, url_prefix="/products")
    app.register_blueprint(inventory_blueprint, url_prefix="/inventory")
    app.register_blueprint(demand_blueprint, url_prefix="/demand")
    app.register_blueprint(distribution_blueprint, url_prefix="/distributions")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
