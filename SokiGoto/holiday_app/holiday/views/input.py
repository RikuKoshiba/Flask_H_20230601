from flask import request, redirect, url_for, render_template, flash, session
from holiday import app
# from holiday.models.entries import Holiday
# from holiday import db


@app.route("/", methods=["GET", "POST"])
def input():
    date = session.pop("date", "")
    title = session.pop("title", "")
    # title = ""
    # date = ""
    print("aaaaaaaaaaa", title, date)
    return render_template("input.html",
                           title=title,
                           date=date)
