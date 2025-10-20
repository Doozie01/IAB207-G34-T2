from flask_wtf import FlaskForm
from wtforms.fields import (TextAreaField, BooleanField, DateTimeLocalField, SubmitField, StringField, PasswordField, EmailField,TelField, FormField, SelectField, IntegerField, DecimalField)
from wtforms.validators import InputRequired, Email, EqualTo, Length, NumberRange
from .models import Category
from flask_wtf.file import FileField, FileAllowed


# ----- REGISTER / LOGIN FORMS ------- #
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
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    name    = FormField(NameForm)   # NameForm (no CSRF)
    email   = EmailField("Email", validators=[Email("Please enter a valid email address")])
    number  = TelField("Phone Number", validators=[InputRequired(), Length(min=10, max=10, message="Please enter a valid Phone Number")])
    address = FormField(AddressForm)  # AddressForm (no CSRF)
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords do not match")])
    confirm  = PasswordField("Confirm Password")
    submit   = SubmitField("Register")

# ----- CREATE EVENT FORMS ------ #

class CreateEventForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=200)])
    description = TextAreaField("Description", validators=[InputRequired(), Length(max=5000)])
    image = FileField("Event Image", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    start_at = DateTimeLocalField("Starts", format="%Y-%m-%dT%H:%M", validators=[InputRequired()])
    end_at   = DateTimeLocalField("Ends",   format="%Y-%m-%dT%H:%M", validators=[InputRequired()])
    venue = StringField("Venue", validators=[InputRequired(), Length(max=150)])
    price = DecimalField("Price (AU$)", validators=[InputRequired(), NumberRange(min=0, message="Price must be above 0$")])
    status = SelectField("Status", choices=[("Open","Open"),("Inactive","Inactive"),("Cancelled","Cancelled")])
    tickets_av = IntegerField("Tickets Available", validators=[NumberRange(min=0)])
    category_id = SelectField("Category", coerce=int, validators=[InputRequired()])
    submit = SubmitField("Create")

    def set_category_choices(self):
        self.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
