from flask import request, redirect, url_for, render_template, abort, flash, session, make_response
from . import user_bp
from datetime import timedelta
from .forms import RegistrationForm
from .models import User
from app import db

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

@user_bp.route("/login")
def login():
    return render_template("login.html")

@user_bp.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    if (username == "admin" and password == "admin"):
        session["user"] = username
        flash("Successful login")
        return redirect(url_for("users.profile"))
    else:
        flash("Invalid username or password")
        return redirect(url_for("users.login"))

@user_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if session.get("user") is not None:
        return render_template("profile.html", cookies=request.cookies.to_dict(), theme=request.cookies.get("theme", "light"))
    else:
        flash("Session error")
        return redirect(url_for("users.login"))

@user_bp.route("/logout")
def logout():
    session.pop("user", default=None)
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