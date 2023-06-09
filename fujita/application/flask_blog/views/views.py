from flask import request, redirect, url_for, render_template, flash, session
from flask_blog import app  # __init__.py が読まれている
from functools import wraps


def login_required(view):
    @wraps(view)
    def inner(*args, **kargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kargs)
    return inner


@app.route("/entries/new", methods=["GET"])
def new_entry():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("entries/new.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            flash("ユーザ名が違います")
        elif request.form["password"] != app.config["PASSWORD"]:
            flash("パスワードが異なります")
        else:
            session["logged_in"] = True
            flash("ログインしました")
            return redirect(url_for("show_entries"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("ログアウトしました")
    return redirect(url_for("show_entries"))
