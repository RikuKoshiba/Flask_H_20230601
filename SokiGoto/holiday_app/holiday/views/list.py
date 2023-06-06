from flask import request, redirect, url_for, render_template, flash, session
from holiday import app
from holiday.models.mst_holiday import Holiday
from holiday import db


@app.route("/list", methods=["POST"])
def list():
    holidays = Holiday.query.order_by(Holiday.holi_date.asc()).all()
    return render_template("list.html", holidays=holidays)
