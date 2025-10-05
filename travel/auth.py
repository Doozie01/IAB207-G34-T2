from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm

authbp = Blueprint('auth', __name__)

@authbp.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        print('Successfully Logged In')
        flash('You Logged in Successfully')
        return redirect(url_for('auth.login'))
    return render_template('user.html', form=loginForm, heading='Login')

@authbp.route('/register', methods = ['GET', 'POST'])
def register():
    registerForm = RegisterForm()
    if registerForm.validate_on_submit():
        print('Successfully Registered')
        return redirect(url_for('auth.login'))
    return render_template('user.html', form=registerForm, heading='Create an Account')