from flask import request, redirect, url_for, render_template, flash, session
import re

from salary import app



@app.route("/")  # # http://xxx 以降のURLパスを '/' と指定
def show_input():
    return render_template("input.html")


@app.route("/output", methods=["GET", "POST"])
def show_output():
    if request.method == "POST":
        if request.form["salary"] == "":
            flash("給与が未入力です。入力してください。")
        elif len(request.form["salary"]) > 10:
            flash("給与には最大9,999,999,999まで入力可能です。")
        elif int(request.form["salary"]) < 0:
            flash("給与にはマイナスの値は入力できません。")
        else:
            threshold = 1000000
            salary = int(request.form["salary"])
            if salary > threshold:
                tax = threshold * 0.1 + (salary - threshold) * 0.2
            else:
                tax = salary * 0.1
            pay = salary - tax
            script = f"給与：{salary}円の場合、支給額：{int(pay)}円、税額：{int(tax)}円です。"
            return render_template("output.html", script=script)

    return redirect(url_for("show_input"))
