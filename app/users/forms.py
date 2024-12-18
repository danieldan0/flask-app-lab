from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from .models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

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

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=60)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=60)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Email not found. Please register first.")
    
    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(password.data):
            raise ValidationError("Incorrect password. Please try again.")

class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=20), Regexp("^[a-zA-Z0-9_.]*$", message="Username must contain only letters, numbers, dots or underscores.")])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=60)])
    image_file = FileField("Update Profile Picture", validators=[FileAllowed(("png", "jpg", "jpeg", "gif", "bmp", "webp"), message="Images only!")])
    about_me = StringField("About Me", validators=[Length(max=140)])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already exists. Please choose a different one.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email already exists. Please choose a different one.")

class UpdatePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[DataRequired(), Length(max=60)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=60)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Update Password")

    def validate_old_password(self, old_password):
        if not current_user.check_password(old_password.data):
            raise ValidationError("Incorrect old password. Please try again.")