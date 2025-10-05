from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, EmailField, TelField
from wtforms.validators import InputRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired('Enter Email')])
    password = PasswordField("Password", validators=[InputRequired('Enter Password')])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    email = EmailField("Email",[Email("Please enter a valid email address")])
    number = TelField("Phone Number", validators=[InputRequired(), Length(min=10, max=10, message="Please enter a valid Phone Number")])
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords do not match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")
