from flask import request, redirect, url_for, render_template, abort, flash, session, make_response, current_app
from . import user_bp
from datetime import timedelta, datetime, timezone
from .forms import RegistrationForm, LoginForm, UpdateAccountForm
from .models import User
from app import db
from flask_login import login_user, logout_user, current_user, login_required
import os
import secrets

@user_bp.before_app_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@user_bp.route("/hi/<string:name>")   #/hi/ivan?age=45&q=fdfdf
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)   

    return render_template("hi.html", 
                           name=name, age=age)

@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)     # "http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("users.account"))
        else:
            flash("Login failed. Please check your email and password", "danger")
            return redirect(url_for("users.login"))
    return render_template("login.html", form=form)

@user_bp.route("/account")
@login_required
def account():
    return render_template("account.html", user=current_user)

@user_bp.route("/users")
def users():
    users = User.query.all()
    return render_template("users.html", users=users)

@user_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if session.get("user_id") is not None:
        user = User.query.get(session["user_id"])
        return render_template("profile.html", user=user, cookies=request.cookies.to_dict(), theme=request.cookies.get("theme", "light"))
    else:
        flash("Session error")
        return redirect(url_for("users.login"))

@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("users.login"))

@user_bp.route("/add_cookie", methods=["POST"])
def add_cookie():
    key = request.form.get("cookie_name")
    value = request.form.get("cookie_value")
    lifespan = request.form.get("cookie_expires")
    response = make_response(redirect(url_for("users.profile")))
    try:
        lifespan = float(lifespan)
        response.set_cookie(key, value, max_age=lifespan)
    except ValueError:
        flash("Invalid cookie lifespan")
    return response
    

@user_bp.route("/delete_cookie", methods=["POST"])
def delete_cookie():
    key = request.form.get("delete_cookie_name")
    response = make_response(redirect(url_for("users.profile")))
    response.delete_cookie(key)
    return response

@user_bp.route("/delete_all_cookies", methods=["POST"])
def delete_all_cookies():
    response = make_response(redirect(url_for("users.profile")))
    for key in request.cookies:
        response.delete_cookie(key)
    return response

@user_bp.route("/set_theme", methods=["POST"])
def set_theme():
    theme = request.form.get("theme")
    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie("theme", theme, max_age=timedelta(days=400))
    return response

@user_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_password = User.hash_password(password)
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = 'pfp/' + random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'users/static/img', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

def delete_picture(picture_file):
    if picture_file and picture_file != "default.png":
        picture_path = os.path.join(current_app.root_path, 'users/static/img', picture_file)
        if os.path.exists(picture_path):
            os.remove(picture_path)

@user_bp.route("/update_account", methods=["GET", "POST"])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        if form.image_file.data:
            delete_picture(current_user.image_file)
            picture_file = save_picture(form.image_file.data)
            current_user.image_file = picture_file
        db.session.commit()
        flash("Account updated", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template("update_account.html", form=form)