from flask import Blueprint, render_template, session, redirect, request

Auth = Blueprint("auth", __name__)

@Auth.route("/login")
def Login():
    return render_template("login.html", title="Movies | Login", theme=session["theme"])

@Auth.route("/register")
def Register():
    return render_template("register.html", title="Movies | Register", theme=session["theme"])