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
            return redirect(url_for('main.index'))
        else:
            print(error)
            flash(error)

        pass
    return render_template('user.html', form=loginForm, heading='Login', mode='login')

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    registerForm = RegisterForm()
    if registerForm.validate_on_submit():
        name = registerForm.name.data                          
        tel = registerForm.number.data
        pwd = registerForm.password.data
        email = registerForm.email.data
        address = registerForm.address.data

        existing_user = User.query.filter_by(emailid=email).first()
        if existing_user:
            flash('Email already registered. Please log in.')
            return redirect(url_for('auth.login'))          

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
    if request.method == 'POST' and not registerForm.validate():
        print('Register errors:', registerForm.errors)
        flash('Please fix the errors below.', 'error')

        pass
    return render_template('user.html', form=registerForm, heading='Create an Account', mode='register')


@authbp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))