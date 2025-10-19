from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

from .import db

authbp = Blueprint('auth', __name__)

@authbp.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    error=None
    if loginForm.validate_on_submit():
        email = loginForm.email.data
        password = loginForm.password.data
        u1 = User.query.filter_by(emailid=email).first()

        if u1 is None:
            error = 'Incorrect Email'
        elif not check_password_hash(u1.password_hash, password):
            error = 'Incorrect Password'
        else:
            login_user(u1)
            return redirect(url_for('main.index'))

        if error is None:
            login_user(u1)
            return redirect(url_for('auth.login'))
        else:
            print(error)
            flash(error)
        return render_template('user.html', form=loginForm, heading='Login')

        login_user(user)
        print('Successfully Logged In')
        flash('You Logged in Successfully')
        next = flask.request.args.get('next')
        if not url_has_allowed_host_and_scheme(next, request.host):
            return abort(400)
        return redirect(next or url_for('auth.login'))
    return render_template('user.html', form=loginForm, heading='Login')

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data                          
        tel = form.number.data
        pwd = form.password.data
        email = form.email.data
        address = form.address.data                    

        pwd_hash = generate_password_hash(pwd)
        new_user = User(
            name=f"{name.get('first_name','').strip()} {name.get('last_name','').strip()}".strip(),
            emailid=email,
            password_hash=pwd_hash,
            phone=str(tel),
            address=f"{address.get('street','')}, {address.get('city','')} {address.get('state','')} {address.get('zip_code','')}".strip()
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Successfully Registered', 'success')
        return redirect(url_for('auth.login'))

    # Debug in terminal
    if request.method == 'POST' and not form.validate():
        print('Register errors:', form.errors)
        flash('Please fix the errors below.', 'error')

    return render_template('register.html', form=form, heading='Create an Account')


@authbp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(active_page="index")