#一覧画面の呼び出し
from flask import request, redirect, url_for, render_template, flash, session
from holiday import app
from holiday.models.mst_holiday import Holiday

@app.route("/list", methods=["POST"])
def list():
    holiday_list = Holiday.query.all()
    return render_template('list.html', holiday_list = holiday_list)