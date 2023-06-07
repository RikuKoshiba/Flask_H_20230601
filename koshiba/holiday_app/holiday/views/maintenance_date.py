from flask import request, redirect, url_for, render_template, flash, session
from holiday import app
from holiday import db
from holiday.models.mst_holiday import Holiday

@app.route('/result', methods=['GET', 'POST'])
def m_result():
    if request.method == 'POST':
        # print(request.form)
        # 登録、更新、削除のデータベース処理、valueによって条件分岐を行う
        if request.form["button"] == "insert_update": # 登録・更新の場合
                holiday = Holiday(
                          holi_date=request.form['holiday'],
                          holi_text=request.form['holiday_text']
                          )
                db.session.merge(holiday)
                db.session.commit()
                return render_template('result.html')
        elif request.form["button"] == "delete":
                holiday = Holiday.query.get(request.form['holiday']) # blogではid、カラムで設定した名前
                if holiday != None:
                      db.session.delete(holiday)
                      db.session.commit()
                      return render_template('result.html')
                else:
                      # flash(f'{holiday}は、祝日マスタに登録されていません') # ここだけ終わってない
                      return render_template('input.html')
        
    





