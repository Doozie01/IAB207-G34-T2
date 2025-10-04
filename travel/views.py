from flask import Blueprint, render_template, url_for

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html', active_page="index")

@bp.route('/search')
def search():
    return render_template('search.html', active_page="search")

@bp.route('/event')
def event():
    return render_template('event.html', active_page="event")
    
@bp.route('/create-event')
def create_event():
    return render_template('create-event.html', active_page="create-event")

@bp.route('/bookings')
def bookings():
    return render_template('bookings.html', active_page="bookings")

@bp.route('/login')
def login():
    return render_template('login.html', active_page="login")

@bp.route('/register')
def register():
    return render_template('register.html', active_page="register")