from dataclasses import asdict
from flask import Blueprint, render_template, session, redirect, request, flash, url_for, current_app
from MyMovie.forms import RegisterForm, LoginForm
from MyMovie.models.models import User
from passlib.hash import pbkdf2_sha256
import uuid

Auth = Blueprint("auth", __name__)

@Auth.route("/login", methods=["GET", "POST"])
def Login():
    form = LoginForm()
    if "theme" not in session:
        session["theme"] = "light"

    if session.get("email"):
        return redirect(url_for("movies.index"))
    
    if form.validate_on_submit():
        user = current_app.db.users.find_one({"email": form.email.data})

        if user and pbkdf2_sha256.verify(form.password.data, user["password_hash"]):
            session["email"] = user["email"]
            flash("Login successful!", "success")
            return redirect(url_for("movies.index"))
        else:
            flash("Invalid email or password. Please try again.", "danger")
            return redirect(url_for("auth.Login"))

    return render_template("login.html", title="Movies | Login", form=form, theme=session["theme"])

@Auth.route("/register", methods=["GET", "POST"])
def Register():
    if "theme" not in session:
        session["theme"] = "light"

    if session.get("email"):
        return redirect(url_for("movies.index"))
    
    form = RegisterForm()

    if form.validate_on_submit():
        if current_app.db.users.find_one({"email": form.email.data}):
            flash("Email already registered. Please log in.", "danger")
            return redirect(url_for("auth.Login"))

        user = User(
            _id = uuid.uuid4().hex,
            email = form.email.data,
            password_hash = pbkdf2_sha256.hash(form.password.data), 
        )

        flash("Registration successful!", "success")

        current_app.db.users.insert_one(asdict(user))

        return redirect(url_for("movies.index"))
    
    return render_template("register.html", title="Movies | Register", form=form ,theme=session["theme"])

@Auth.route("/logout")
def Logout():
    session.pop("email", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.Login"))