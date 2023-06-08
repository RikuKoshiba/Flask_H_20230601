from flask import render_template
from holiday import app  # __init__.py が読まれている
# from holiday import db
from holiday.models.mst_holidays import Holiday


@app.route("/list", methods=["GET"])
def show_list():
    holidays = Holiday.query.order_by(Holiday.holi_date.desc()).all()
    return render_template("list.html", holidays=holidays)
