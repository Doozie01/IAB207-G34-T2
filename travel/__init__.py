from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager

db = SQLAlchemy()

# Next line is for testing purposes
from .models import User


def create_app():
    app = Flask(__name__)
<<<<<<< HEAD
=======
    app.secret_key = 'secret'
>>>>>>> origin/main

    # DB configuration and initialisation
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traveldb.sqlite'
    db.init_app(app)


    Bootstrap5(app)

    from .views import bp as main_bp
    app.register_blueprint(main_bp)
    from . import auth
    app.register_blueprint(auth.authbp)

    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    from.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app