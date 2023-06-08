# from flask import request, redirect, url_for, render_template, flash, session
from flask import render_template, session
from holiday import app  # __init__.py が読まれている
# from functools import wraps


@app.route("/", methods=["GET"])
def show_input():
    return render_template("input.html")


@app.route("/result")
def show_result():
    return render_template("result.html", msg=session.get("message"))
