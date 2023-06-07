from flask import request, redirect, url_for, render_template, flash, session
from holiday import app


@app.route('/')
def input():
    return render_template("input.html")

