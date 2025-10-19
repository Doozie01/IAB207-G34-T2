from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, EmailField, TelField, FormField, SelectField, IntegerField
from wtforms.validators import InputRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired('Enter Email')])
    password = PasswordField("Password", validators=[InputRequired('Enter Password')])
    submit = SubmitField("Login")

class NameForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class AddressForm(FlaskForm):
    street = StringField("Address Line", validators=[InputRequired()])
    city =  StringField("City", validators=[InputRequired()])
    state = SelectField("State", choices=[('QLD'), ('NSW'), ('VIC'), ('WA'), ('SA'), ('NT'), ('ACT'), ('TAS')], validators=[InputRequired()])
    zip_code = IntegerField("Zip Code", validators=[InputRequired(), Length(min=4, max=4, message="Please enter a real zip code")])

class RegisterForm(FlaskForm):
    name = FormField(NameForm)
    email = EmailField("Email",[Email("Please enter a valid email address")])
    number = TelField("Phone Number", validators=[InputRequired(), Length(min=10, max=10, message="Please enter a valid Phone Number")])
    address = FormField(AddressForm)
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords do not match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")