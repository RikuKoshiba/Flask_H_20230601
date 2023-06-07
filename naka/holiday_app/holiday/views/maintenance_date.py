#データベース処理、その後の結果画面呼び出し
from flask import request, redirect, url_for, render_template, flash, session
from holiday import app
from holiday.models.mst_holiday import Holiday
from holiday import db

@app.route('/result', methods=['POST'])
def maintenance_date():
    holiday_date = request.form["holiday"]
    holiday_text = request.form["holiday_text"]

    #新規登録・更新ボタン押下
    if request.form["button"] == "insert_update":
      if len(holiday_text) > 20:
        flash('テキストは20文字以内で入力してください')
        return redirect('/')
      if holiday_text == "" or holiday_date == "":
        flash('空欄があります')
        return redirect('/')
      holiday = Holiday.query.get(holiday_date)
      data = Holiday(
        holi_date = holiday_date,
        holi_text = holiday_text
      )

      #存在しないなら追加
      if holiday is None:
        db.session.add(data)
        db.session.commit()
        msg = f'{holiday_date}（{holiday_text}）が登録されました'

      #存在したら更新
      else:
        db.session.merge(data)
        db.session.commit()
        msg = f'{holiday_date}は{holiday_text}に更新されました'
      return render_template('/result.html', msg = msg)

    #削除ボタン押下
    elif request.form["button"] == "delete":
      if holiday_date == "":
        flash('日付を入力してください')
        return redirect('/')

      holiday = Holiday.query.get(holiday_date)
      data = Holiday(
        holi_date = holiday_date,
        holi_text = holiday_text
      )

      if holiday is None:
       flash(f'{holiday_date}は、祝日マスタに登録されていません')
       return redirect('/')
      else:
        db.session.delete(holiday)
        db.session.commit()
        #成功したら
        msg = f'{holiday.holi_date}({holiday.holi_text})は、削除されました'
        return render_template('/result.html', msg = msg)
