from flask import request, redirect, url_for, render_template, flash, session
import re
from flask_blog import app
from flask_blog.models.users import Users
from flask_blog import db
from functools import wraps
import os
import hashlib
import base64


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
        loginid = request.form["loginid"]
        password = request.form["password"]
        user = Users.query.filter(Users.loginid == loginid).first()
        if user is None:
            flash("ユーザ名が異なります")
            return render_template("login.html")

        salt, hash_val = sep_salt_hash(user.password)
        mk_hash_val = password_hash(password, salt.encode("utf-8"))
        if hash_val != mk_hash_val:
            flash("パスワードがことなります")
        else:
            session["logged_in"] = True
            session["user_id"] = user.id
            session["loginid"] = user.loginid
            flash("ログインしました")
            return redirect(url_for("show_entries"))
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        if request.form["befor_page"] == "signup":
            loginid = request.form["loginid"]
            password = request.form["password"]
            user = Users.query.filter(Users.loginid == loginid).first()
            if user is not None:
                flash("すでに存在するユーザーです")
                return render_template("signup.html")
            if not re.match(r"^\w+$", loginid):
                flash("ユーザ名は英字大文字と英字小文字と数字のみで入力してください")
                return render_template("signup.html")
            if not re.match(r"^[a-zA-Z0-9#$%&]+$", password):
                flash("パスワードは英字大文字、英字小文字、数字、#、$、%、&のみで入力してください")
                return render_template("signup.html")
            salt = base64.b64encode(os.urandom(32))
            pass_hash = salt.decode("utf-8") + \
                "$" + password_hash(password, salt)
            user = Users(
                loginid=loginid,
                password=pass_hash
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


@app.route("/profile/<int:user_id>", methods=["GET"])
def profile(user_id):
    login_user_id = session.get("user_id")
    userinfo = Users.query.filter(Users.id == user_id).first()
    print(userinfo, login_user_id)
    return render_template("profile.html",
                           user=userinfo,
                           login_user_id=login_user_id)


@app.route("/profile/edit", methods=["POST"])
@login_required
def profile_edit():
    return render_template("profile_edit.html")


@app.route("/profile/update", methods=["POST"])
def profile_update():
    username = session.get("username")

    file = request.files['example']
    filename = base64.b64encode(os.urandom(32)).decode("utf-8")
    file.save(os.path.join('./static/image', filename))
    
    return redirect(url_for("profile"), username)


def password_hash(password, salt):
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        app.config["HASH_NUM"]
            ).hex()
    # print(password_hash)
    return password_hash


def sep_salt_hash(pass_hash):
    res = re.match(r"^(.*)\$(.*)$", pass_hash)
    salt = res[1]
    hash_val = res[2]
    return salt, hash_val


def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].\
        lower() in app.config("ALLOWED_EXTENSIONS")
