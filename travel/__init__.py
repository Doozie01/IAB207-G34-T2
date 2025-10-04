from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .views import bp as main_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)


    # DB configuration and initialisation
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traveldb.sqlite'
    db.init_app(app)

    app.register_blueprint(main_bp)

    return app