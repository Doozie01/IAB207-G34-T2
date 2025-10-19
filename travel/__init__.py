from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY='secret',
        SQLALCHEMY_DATABASE_URI='sqlite:///traveldb.sqlite',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    Bootstrap5(app)

    from . import models

    from .views import bp as main_bp
    app.register_blueprint(main_bp)

    from .auth import authbp
    app.register_blueprint(authbp)

    with app.app_context():
        from . import models
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id: str):
        from .models import User
        return User.query.get(int(user_id))

    return app
