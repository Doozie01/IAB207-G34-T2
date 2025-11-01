from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from datetime import datetime
import os

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 # 5 MB LIMIT
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

    # create tables
    with app.app_context():
        from . import models
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id: str):
        from .models import User
        return User.query.get(int(user_id))

    @app.cli.command("seed")
    def seed():
        """Seed the database with demo data."""
        from datetime import datetime, timedelta
        from werkzeug.security import generate_password_hash
        from .models import User, Category, Event, db

        db.drop_all()
        db.create_all()

        # demo user
        user = User.query.filter_by(emailid="demo@expertrelay.dev").first()
        if not user:
            user = User(
                name="Demo User",
                emailid="demo@expertrelay.dev",
                password_hash=generate_password_hash("password123"),
                phone="0412345678",
                address="123 Demo St, Brisbane QLD 4000",
            )
            db.session.add(user)

        # categories
        names = ["Business","Technology","Marketing","Art","Science",
                 "Teaching","Lifestyle","Health","Regulation"]
        cats = {}
        for n in names:
            c = Category.query.filter_by(name=n).first()
            if not c:
                c = Category(name=n)
                db.session.add(c)
            cats[n] = c

        db.session.flush()  # get IDs

        # events
        now = datetime.now()
        def add_event(title, desc, cat, days, venue="QUT Gardens Point",
                      price = 60, status="Open", tickets=50, img=None):
            if Event.query.filter_by(title=title).first():
                return
            start = now + timedelta(days=days)
            end = start + timedelta(hours=2)
            e = Event(
                title=title,
                description=desc,
                image=img,
                start_at=start,
                end_at=end,
                venue=venue,
                price=price,
                status=status,
                tickets_av=tickets,
                user_id=user.id,
                category_id=cats[cat].id
            )
            db.session.add(e)

        add_event("Intro to Bootstrap", "Learn Bootstrap 5 in Flask!", "Technology", 3, img="HowToBootstrap.png")
        add_event("Marketing Yourself", "Portfolio marketing strategies.", "Marketing", 6, venue="QUT Kelvin Grove", img="MarketingYourWebsite.png")
        add_event("UML & ERD Practice", "Hands-on diagramming.", "Science", 10, status="Cancelled", img="UMLDiagram.png")
        add_event("Video Editting 101", "Easy tutorial for how to edit videos.", "Art", 14, price = 30.3, img="VideoEditing.jpg")

        db.session.commit()
        print("Database seeded.")

    @app.before_request
    def sync_event_status():
        from datetime import datetime
        from .models import Event
        
        now = datetime.now()
        to_update = Event.query.filter(
            (Event.end_at < now) | (Event.tickets_av <= 0) | (Event.status == "Open")
        ).all()
        changed = False
        for ev in to_update:
            prev = ev.status
            ev.persist_live_status()
            if ev.status != prev:
                changed = True
        if changed:
            db.session.commit()

    return app
