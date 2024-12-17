from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=20), Regexp("^[a-zA-Z0-9_.]*$", message="Username must contain only letters, numbers, dots or underscores.")])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=60)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=60)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists. Please choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists. Please choose a different one.")