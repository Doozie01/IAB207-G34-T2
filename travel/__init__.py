from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5

db = SQLAlchemy()

# Next line is for testing purposes
from .models import User


def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret'

    # DB configuration and initialisation
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traveldb.sqlite'
    db.init_app(app)


    Bootstrap5(app)

    from .views import bp as main_bp
    app.register_blueprint(main_bp)
    from . import auth
    app.register_blueprint(auth.authbp)

    return app