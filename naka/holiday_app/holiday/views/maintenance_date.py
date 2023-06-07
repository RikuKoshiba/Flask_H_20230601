#データベース処理、その後の結果画面呼び出し
from flask import request, redirect, url_for, render_template, flash, session
from holiday import app
from holiday.models.mst_holiday import Holiday

@app.route('/list')
def list():
  holidays = Holiday.query.order_by(Holiday.holi_date.desc()).all()
  return render_template('/list')