from flask_blog import app
from flask import request, redirect, url_for, render_template, flash, session


@app.route("/")
def show_entries():
    return render_template("entries/index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            print("ユーザ名が異なります")
        elif request.form["password"] != app.config["PASSWORD"]:
            print("パスワードがことなります")
        else:
            return redirect("/")
    return render_template("entries/login.html")


@app.route("/logout")
def logout():
    return redirect("/")


@app.route("/user/<username>")
def userPage(username):
    return f"{username} page"
