from flask import Blueprint, render_template, url_for, request, session, redirect, flash, current_app
from flask_login import login_required, current_user
from .models import Event, Comment, Category, Order
from . import db
from .forms import CreateEventForm
from werkzeug.utils import secure_filename
from sqlalchemy import or_
from datetime import datetime
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
    qtext = request.args.get('q','', type=str)
    cat_id = request.args.get('cat',type=int)

    query =db.session.query(Event).outerjoin(Category)

    if qtext:
        like = f"%{qtext.strip()}%"
        query = query.filter(or_(
            Event.title.ilike(like),
            Event.description.ilike(like),
            Event.venue.ilike(like),
            Category.name.ilike(like),
        ))

    if cat_id:
        query = query.filter(Event.category_id == cat_id)
    
    events = query.order_by(Event.start_at.asc()).all()

    categories = Category.query.order_by(Category.name.asc()).all()
    active_category = Category.query.get(cat_id) if cat_id else None

    return render_template(
        'search.html',
        q=qtext,
        events=events,
        categories=categories,
        active_category=active_category,
        results_count=len(events),
        active_page="search"
        )


@bp.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    if request.method =="POST":
        current_user.name=request.form.get("name")
        current_user.emailid=request.form.get("email")
        current_user.phone=request.form.get("phone")
        current_user.address=request.form.get("address")
        db.session.commit()
        flash("Profile updated successfully!","success")
        return redirect(url_for("main.profile"))
    return render_template('profile.html', user=current_user, active_page="profile")

@bp.route('/event/<int:event_id>', methods=['GET','POST'])
def event_detail(event_id):
    from .models import Event
    event = Event.query.get_or_404(event_id)
    comments = Comment.query.filter_by(event_id=event_id).order_by(Comment.posted_at.desc()).all()

    # Handle comment submission
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))

        text = request.form.get('comment')
        if text:
            new_comment = Comment(
                text=text,
                user_id=current_user.id,
                event_id=event_id
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('main.event_detail', event_id=event_id))
        
    return render_template('event.html', event=event, comments=comments, active_page="event")
    
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
            price=form.price.data,
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
@login_required
def bookings():
    now = datetime.now()

    orders = (
        Order.query
        .join(Event)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )

    upcoming_orders = [o for o in orders if o.event.start_at >= now]
    past_orders = [o for o in orders if o.event.start_at < now]

    return render_template('bookings.html', upcoming=upcoming_orders, past=past_orders, active_page="bookings")



@bp.route('/confirm/<int:event_id>', methods=['GET','POST'])
@login_required
def confirm(event_id):
    event = Event.query.get_or_404(event_id)
    quantity = int(request.args.get('quantity', session.get('booking_quantity', 1)))
    total = quantity * event.price

    if request.method == 'POST':
        order = Order(
            user_id=current_user.id,
            event_id=event.id,
            quantity=quantity,
            total_amount=total
        )

        if quantity > event.tickets_av:
            flash("Not enough tickets available.", "danger")
            return redirect(url_for('main.event_detail', event_id=event.id))

        event.tickets_av -= quantity
        db.session.add(order)
        db.session.commit()
        session.pop('booking_quantity', None)
        return redirect(url_for('main.bookings'))

    return render_template('confirm.html', event=event, quantity=quantity, total=total, active_page="confirm")
