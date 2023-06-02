from salary_calc import app
from flask import request, redirect, url_for, render_template, flash, session
from currency_converter import CurrencyConverter


@app.route("/", methods=["GET", "POST"])
def input():
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # sessionを使う方法
    salary = session.pop("salary", "")
    currency = session.pop("currency", "JPY")
    # ===========================================
    # sessionを使わない方法
    # salary = request.args.get("salary")
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    curcon = CurrencyConverter()
    currencies = curcon.currencies
    return render_template("input.html",
                           before_salary=salary,
                           currencies=currencies,
                           selected_currency=currency)


@app.route("/output", methods=["GET", "POST"])
def output():
    if request.method != "POST":
        return redirect(url_for("input"))

    if request.form["salary"] == "":
        flash("給料が未記入です")
        return redirect(url_for("input"))

    input_salary = int(request.form["salary"])
    currency = request.form["currency"]
    curcon = CurrencyConverter()
    salary = int(curcon.convert(input_salary, currency, 'JPY'))

    if salary > 9999999999:
        if currency != "JPY":
            flash("給与には最大9,999,999,999円まで入力可能です。\n" +
                  f"{input_salary:,}{currency}は{salary:,}円です。")
        else:
            flash("給与には最大9,999,999,999円まで入力可能です。")
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # sessionを使う方法
        session["salary"] = input_salary
        session["currency"] = currency
        return redirect(url_for("input"))
        # ===========================================
        # sessionを使わない方法
        # return redirect(url_for("input", salary=salary))
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    if salary < 0:
        flash("整数値を入力してください")
        return redirect(url_for("input"))

    if salary > 1000000:
        tax = 1000000 * 0.1 + (salary - 1000000) * 0.2
        pay = salary - tax
    else:
        tax = salary * 0.1
        pay = salary - tax
    text = f"給与：{salary:,}円、支給：{int(pay):,}円、税額：{int(tax):,}円です。"
    return render_template("output.html", text=text)
