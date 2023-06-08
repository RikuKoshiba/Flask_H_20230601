from flask import request, render_template, redirect, url_for, flash, session
from holiday import app  # __init__.py が読まれている
from holiday import db
import datetime
from holiday.models.mst_holidays import Holiday


@app.route("/create", methods=["GET", "POST"])
def update_holiday():
    if request.method == "POST":
        if request.form["holiday"] == "":
            flash("日付が入力されていません")
            redirect(url_for("show_input"))
        elif request.form["holiday_text"] == "":
            flash("テキストが入力されていません")
            redirect(url_for("show_input"))
        elif len(request.form["holiday_text"]) > 20:
            flash("テキストは１～２０文字で入力してください")
            redirect(url_for("show_input"))
        else:
            holidays = Holiday.query.all()
            tdates = [holidays[i].holi_date for i in range(len(holidays))]

            tstr = request.form["holiday"]
            tdatetime = datetime.datetime.strptime(tstr, '%Y-%m-%d')
            tdate = datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)
            if request.form["button"] == "insert_update":
                if tdate in tdates:
                    holiday = Holiday.query.get(request.form["holiday"])
                    holiday.holi_text = request.form["holiday_text"]
                    db.session.merge(holiday)
                    db.session.commit()
                    session["message"] = f"{request.form['holiday']}は{request.form['holiday_text']}に更新されました"
                    return redirect(url_for("show_result"))
                else:
                    holiday = Holiday(
                        holi_date=request.form["holiday"],
                        holi_text=request.form["holiday_text"]
                    )
                    db.session.add(holiday)
                    db.session.commit()
                    session["message"] = f"{request.form['holiday']}（{request.form['holiday_text']}）が登録されました"
                    return redirect(url_for("show_result"))

            elif request.form["button"] == "delete":
                if tdate in tdates:
                    holiday = Holiday.query.get(request.form["holiday"])
                    db.session.delete(holiday)
                    db.session.commit()
                    session["message"] = f"{request.form['holiday']}（{request.form['holiday_text']}）は削除されました"
                    return redirect(url_for("show_result"))
                else:
                    flash(f"{request.form['holiday']}は祝日マスタに登録されていません")
                    redirect(url_for("show_input"))

    return render_template("input.html")
