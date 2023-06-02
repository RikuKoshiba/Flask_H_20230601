from salary import app
from flask import request, redirect, url_for, render_template, flash, session
from decimal import Decimal, ROUND_HALF_UP


@app.route("/", methods=["GET", "POST"]) #GET:直接ポストうち POST：form action method= で呼び出されたとき
def input():
    return render_template("input.html") #htmlファイルを作ってウェブへ


@app.route("/output", methods=["GET", "POST"])
def output():
    if request.method != "POST":
        return redirect(url_for("input"))

    if request.form["salary"] == "":
        flash("給料が未記入です")
        return redirect(url_for("input"))

    price = int(request.form["salary"])
    tax = 0
    #100万以上の場合
    if price > 1000000:
        tax = (price - 1000000) / 5
        tax = tax + 100000
    #100万以下の場合
    else:
        tax = price / 10
    tax = Decimal(str(tax)).quantize(Decimal("0"),rounding=ROUND_HALF_UP)

    salary_text = "支給額:" + str(price - tax) + "、税額:" + str(tax)

    return render_template("output.html", text = salary_text)