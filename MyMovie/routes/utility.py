from flask import Blueprint, render_template, session, redirect, request

Util = Blueprint("util", __name__)

@Util.route("/toggle-mode")
def toggle():
    theme = session.get("theme")
    if theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"
    return redirect(request.args.get("current_page"))