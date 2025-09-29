from flask import Flask
from flask_bootstrap import Bootstrap5

def create_app():
    app = Flask(__name__)
    
    Bootstrap5(app)
    
    #add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    app.register_blueprint(dest_bp)
    app.register_blueprint(authbp)

    return app