from flask import Blueprint, render_template, url_for, request, session
from flask_login import login_required, current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html', active_page="index")
    if 'email' in session:
        str = f"Welcome to [blank], {session['email']}"
    else:
        str = "<h1>[blank]<h1>"
    return str

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