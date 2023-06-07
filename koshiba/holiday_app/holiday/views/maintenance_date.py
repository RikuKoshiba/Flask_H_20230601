from flask import request, redirect, url_for, render_template, flash, session
from holiday import app
from holiday import db
from holiday.models.mst_holiday import Holiday


@app.route('/result', methods=['GET', 'POST'])
def m_result():
    if request.method == 'POST':
        # 登録、更新、削除のデータベース処理、valueによって条件分岐を行う
        if request.form["button"] == "insert_update": # 登録・更新の場合
                holiday = Holiday(
                    holi_date=request.form['holiday'],
                    holi_text=request.form['holiday_text']
                )
                db.session.add(holiday)
                db.session.commit()
        elif request.form["button"] == "delate":
                holiday = Holiday.query.get()
                db.session.delete(holiday)
                db.session.commit()
        return render_template('result.html')

# # 登録するデータの編集
# holiday = Holiday(
#     holi_date = date(2024, 1, 1),
#     holi_text = "お正月"
# )

# # INSERT処理
# session.add(holiday)

# # コミット
# session.commit()