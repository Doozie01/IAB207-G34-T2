from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15))
    address = db.Column(db.String(100), index=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # relationships
    comments = db.relationship(
        'Comment',
        back_populates='user',
        cascade='all, delete-orphan'
    )
    orders = db.relationship('Order', backref='user')
    events = db.relationship('Event', backref='user')

    def __repr__(self):
        return f"Name: {self.name}"


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True, nullable=False)
    description = db.Column(db.String(400))
    image = db.Column(db.String(255), nullable=True)   # <-- fix double assignment
    start_at = db.Column(db.DateTime, nullable=False)
    end_at = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    tickets_av = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    comments = db.relationship(
        'Comment',
        back_populates='event',
        cascade='all, delete-orphan'
    )
    orders = db.relationship('Order', backref='event')

    def __repr__(self):
        return f"Event title: {self.title}"
    
    @property
    def live_status(self):
        s = (self.status or "").strip().lower()
        if s == "cancelled":
            return "Cancelled"
        if self.end_at and self.end_at < datetime.now():
            return "Inactive"
        if self.tickets_av is not None and self.tickets_av <= 0:
            return "Sold Out"
        return "Open"
    
    def persist_live_status(self):
        self.status = self.live_status


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400), nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    # back_populates pairs
    user = db.relationship('User', back_populates='comments')
    event = db.relationship('Event', back_populates='comments')

    def __repr__(self):
        return f"Comment: {self.text}"


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Numeric, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Order ID: {self.id}"


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    events = db.relationship('Event', backref='category')

    def __repr__(self):
        return f"Category: {self.name}"
