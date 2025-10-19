from flask_wtf import FlaskForm
from wtforms.fields import (TextAreaField, SubmitField, StringField, PasswordField, EmailField,TelField, FormField, SelectField, IntegerField)
from wtforms.validators import InputRequired, Email, EqualTo, Length, NumberRange

# ----- Subforms (CSRF disabled) ----- #

class NameForm(FlaskForm):
    class Meta:
        csrf = False
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name  = StringField("Last Name",  validators=[InputRequired()])

class AddressForm(FlaskForm):
    class Meta:
        csrf = False
    street   = StringField("Address Line", validators=[InputRequired()])
    city     = StringField("City", validators=[InputRequired()])
    state    = SelectField("State", choices = [(s, s) for s in ['QLD', 'NSW', 'VIC', 'WA', 'SA', 'NT', 'ACT', 'TAS']], validators=[InputRequired()])
    zip_code = IntegerField("Zip Code",validators=[InputRequired(), NumberRange(min=1000, max=9999, message="Please enter a real zip code")])

# ----- Top-level forms ----- #

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired('Enter Email')])
    password = PasswordField("Password", validators=[InputRequired('Enter Password')])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    name    = FormField(NameForm)   # NameForm (no CSRF)
    email   = EmailField("Email", validators=[Email("Please enter a valid email address")])
    number  = TelField("Phone Number", validators=[InputRequired(), Length(min=10, max=10, message="Please enter a valid Phone Number")])
    address = FormField(AddressForm)  # AddressForm (no CSRF)
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords do not match")])
    confirm  = PasswordField("Confirm Password")
    submit   = SubmitField("Register")
