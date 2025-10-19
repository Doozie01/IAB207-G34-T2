from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from .models import db, User, Category, Event

def seed():
    # 1) demo user (owner for seeded events)
    demo = User.query.filter_by(emailid="demo@expertrelay.dev").first()
    if not demo:
        demo = User(
            name="Demo User",
            emailid="demo@expertrelay.dev",
            password_hash=generate_password_hash("password123"),
            phone="0412345678",
            address="123 Demo St, Brisbane QLD 4000",
        )
        db.session.add(demo)

    # 2) categories (id, name table)
    cat_names = [
        "Business","Technology","Marketing","Art","Science",
        "Teaching","Lifestyle","Health","Regulation"
    ]
    cats = {}
    for name in cat_names:
        c = Category.query.filter_by(name=name).first()
        if not c:
            c = Category(name=name)
            db.session.add(c)
        cats[name] = c

    db.session.flush()  # get ids for new rows without full commit

    # 3) events — a few per category
    now = datetime.now()
    def add_event(title, desc, cat_name, days_from_now, hrs=2, venue="QUT Gardens Point",
                  status="Open", tickets=50, img=None):
        start = now + timedelta(days=days_from_now)
        end   = start + timedelta(hours=hrs)
        exists = Event.query.filter_by(title=title).first()
        if exists: 
            return
        e = Event(
            title=title,
            description=desc,
            image=img or + title.replace(" ","-") + "/800/450",
            start_at=start,
            end_at=end,
            venue=venue,
            status=status,
            tickets_av=tickets,
            user_id=demo.id,
            category_id=cats[cat_name].id
        )
        db.session.add(e)

    add_event("How to use Bootstrap for dynamic websites – Tutorial",
              "Learn Bootstrap components and layouts to make your site pop.",
              "Technology", 3)

    add_event("Marketing yourself through your website",
              "Hands-on workshop to identify methods of marketing your portfolio.",
              "Marketing", 6, venue="QUT Kelvin Grove")

    add_event("UML and ERD Diagram Practice",
              "Practical session on UML/ERD with real examples.",
              "Science", 10, status="Cancelled")

    add_event("What is Bootstrap?",
              "Intro session covering the basics of Bootstrap 5.",
              "Technology", 1, tickets=120)

    add_event("Beginner’s Watercolour",
              "A relaxing intro to watercolour techniques.",
              "Art", 14)

    db.session.commit()
    return {"user": demo.emailid, "categories": len(cats), "done": True}
