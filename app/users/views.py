from flask import request, redirect, url_for, render_template, abort, flash, session
from . import user_bp

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

@user_bp.route("/profile")
def profile():
    if session.get("user") is not None:
        return render_template("profile.html")
    else:
        flash("Session error")
        return redirect(url_for("users.login"))

@user_bp.route("/logout")
def logout():
    session.pop("user", default=None)
    return redirect(url_for("users.login"))