from flask import Blueprint, render_template, redirect, url_for, flash
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
        u1 = User.query.filter_by(name=email).first()

        if u1 is None:
            error='Incorrect Email'
        elif not check_password_hash(u1.password_hash, password):
            error='Incorrect Password'

        if error is None:
            login_user(u1)
            return redirect(url_for('auth.login'))
        else:
            print(error)
            flash(error)
        return render_template('user.html', form=loginForm, heading='Login')

@authbp.route('/register', methods = ['GET', 'POST'])
def register():
    registerForm = RegisterForm()
    if registerForm.validate_on_submit():
        
        name = registerForm.name.data
        tel = registerForm.number.data
        pwd = registerForm.password.data
        email = registerForm.email.data
        address = registerForm.address.data

        pwd_hash = generate_password_hash(pwd)
        new_user = User(name=name, password_hash=pwd_hash, emailid=email, phone=tel)
        db.session.add(new_user)
        db.session.commit()

        print('Successfully Registered')

        return redirect(url_for('auth.login'))
    return render_template('user.html', form=registerForm, heading='Create an Account')

@authbp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(active_page="index")