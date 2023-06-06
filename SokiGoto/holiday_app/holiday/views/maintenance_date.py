from flask import request, redirect, url_for, render_template, flash, session
from holiday import app
from datetime import datetime, date
from holiday import db
from holiday.models.mst_holiday import Holiday


@app.route("/maintenance_date", methods=["POST"])
def maintenance_date():
    date_str = request.form["date"]
    datetime_type = datetime.strptime(date_str, "%Y-%m-%d")
    date_type = date(datetime_type.year,
                     datetime_type.month,
                     datetime_type.day)
    title = request.form["title"]
    if request.form["button"] == "insert_update":

        if not check_string_length(title, 20):
            flash("祝日 テキストは、1~20文字以内で入力してください")
            session["date"] = date_str
            session["title"] = title
            return redirect(url_for("input"))

        query = Holiday.query.get(date_type)
        if query is None:
            holiday = Holiday(
                holi_date=date_type,
                holi_text=title
                )
            db.session.add(holiday)
            db.session.commit()
            message = f"{date_type}({title})が登録されました"
            return render_template("result.html",
                                   message=message)
        else:
            query.holi_date = date_type
            query.holi_text = title
            db.session.merge(query)
            db.session.commit()
            message = f"{date_type}は「{title}」に変更されました"
            return render_template("result.html",
                                   message=message)
    elif request.form["button"] == "delete":
        holiday = Holiday.query.get(date_type)
        if holiday is None:
            flash(f"{date_type}は、祝日マスタに登録されていません")
            print("delete miss")
            return redirect(url_for("input"))

        else:
            title = holiday.holi_text
            db.session.delete(holiday)
            db.session.commit()
            message = f"{date_type}({title})は、削除されました"
            return render_template("result.html", message=message)
    else:
        print(request.form["button"])
        return redirect(url_for('input'))


def check_string_length(string, length):
    if 0 < len(string) and len(string) <= length:
        return True
    else:
        return False
