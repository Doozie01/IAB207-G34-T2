from flask import Blueprint, render_template, url_for, request, session, redirect, flash, current_app
from flask_login import login_required, current_user
from .models import Event, Category
from . import db
from .forms import CreateEventForm
from werkzeug.utils import secure_filename
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    cat_id = request.args.get("cat", type=int)
    categories  = Category.query.order_by(Category.name).all()
    events=Event.query.all()
    if cat_id:
        events = Event.query.filter_by(category_id=cat_id).order_by(Event.start_at).all()
        active_category = Category.query.get(cat_id)
    else:
        events = Event.query.order_by(Event.start_at).all()
        active_category=None
    return render_template('index.html', categories=categories, events=events, active_category=active_category, active_page="index")



@bp.route('/search')
def search():
    return render_template('search.html', active_page="search")

@bp.route('/event')
def event():
    return render_template('event.html', active_page="event")
    
@bp.route('/create-event', methods=['GET','POST'])
@login_required
def create_event():
    form = CreateEventForm()
    form.set_category_choices()

    if form.validate_on_submit():
        # --- Handle image upload ---
        image_file = form.image.data
        filename = None

        if image_file:
            # Ensure a safe, unique filename
            filename = secure_filename(image_file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image_file.save(upload_path)

        # --- Create event record ---
        ev = Event(
            title=form.title.data,
            description=form.description.data,
            image=filename,  # store filename only
            start_at=form.start_at.data,
            end_at=form.end_at.data,
            venue=form.venue.data,
            status=form.status.data,
            tickets_av=form.tickets_av.data or 0,
            user_id=current_user.id,
            category_id=form.category_id.data
        )

        db.session.add(ev)
        db.session.commit()

        flash("Event created successfully!", "success")
        return redirect(url_for("main.index"))

    return render_template("create-event.html", form=form, active_page="create-event")

@bp.route('/bookings')
def bookings():
    return render_template('bookings.html', active_page="bookings")

# @bp.route('/login')
# def login():
#     return render_template('login.html', active_page="login")

# @bp.route('/register')
# def register():
#     return render_template('register.html', active_page="register")
