from flask import request, redirect, url_for, render_template, flash, session
import re
from flask_blog import app
from flask_blog.models.users import Users
from flask_blog import db
from functools import wraps


def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return inner


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = Users.query.filter(Users.username == username).first()
        if user is None:
            flash("ユーザ名が異なります")
        elif user.password != password:
            flash("パスワードがことなります")
        else:
            session["logged_in"] = True
            session["user_id"] = user.id
            session["username"] = user.username
            flash("ログインしました")
            return redirect(url_for("show_entries"))
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        if request.form["befor_page"] == "signup":
            username = request.form["username"]
            password = request.form["password"]
            user = Users.query.filter(Users.username == username).first()
            if user is not None:
                flash("すでに存在するユーザーです")
                return render_template("signup.html")
            if not re.match(r"^\w+$", username):
                flash("ユーザ名は英字大文字と英字小文字と数字のみで入力してください")
                return render_template("signup.html")
            if not re.match(r"^[a-zA-Z0-9#$%&]+$", password):
                flash("パスワードは英字大文字、英字小文字、数字、#、$、%、&のみで入力してください")
                return render_template("signup.html")
            user = Users(
                username=username,
                password=password
                )
            db.session.add(user)
            db.session.commit()
            flash("アカウントが制作されました。")
            return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("id", None)
    session.pop("username", None)
    flash("ログアウトしました")
    return redirect(url_for("show_entries"))
