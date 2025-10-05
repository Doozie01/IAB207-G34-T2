from flask import Flask
from .views import bp as main_bp
from flask_bootstrap import Bootstrap5

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.secret_key = 'secret'
    Bootstrap5(app)

    from . import auth
    app.register_blueprint(auth.authbp)

    return app