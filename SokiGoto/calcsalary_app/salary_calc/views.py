from salary_calc import app
from flask import request, redirect, url_for, render_template, flash, session


@app.route("/", methods=["GET", "POST"])
def input():
    return render_template("input.html")


@app.route("/output", methods=["GET", "POST"])
def output():
    if request.method != "POST":
        return redirect(url_for("input"))

    if request.form["salary"] == "":
        flash("給料が未記入です")
        return redirect(url_for("input"))

    salary = int(request.form["salary"])

    if salary < 0:
        flash("整数値を入力してください")
        return redirect(url_for("input"))

    if salary > 1000000:
        tax = 1000000 * 0.1 + (salary - 1000000) * 0.2
        pay = salary - tax
    else:
        tax = salary * 0.1
        pay = salary - tax
    text = f"給与：{salary:,}、支給：{int(pay):,}、税額：{int(tax):,}です。"
    return render_template("output.html", text=text)
