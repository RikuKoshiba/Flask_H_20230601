import math
from flask import request, redirect, url_for, render_template, flash, session
from salary import app

@app.route('/')
def input():
    return render_template("input.html")   

@app.route('/output', methods = ['GET', 'POST'])
def output():
    input_salary = request.form['salary']

    if request.method == 'POST':
        if input_salary == "":
            flash('給与が未入力です。入力してください。')
            return redirect(url_for('input'))
        
        int_input_salary = int(input_salary)
        if int_input_salary > 9999999999:
            flash('給与には最大9,999,999,999まで入力可能です。')
            return redirect(url_for('input'))

        if int_input_salary < 0:
            flash('給与にはマイナスの値は入力できません。')
            return redirect(url_for('input'))

        if int_input_salary > 1000000:
            over = int_input_salary - 1000000
            tax =  over * 0.2 + 100000
        else:
            tax = int_input_salary * 0.1

        # 小数点切り上げ
        tax = math.floor(tax)
        pay = int_input_salary - tax
        
        text = f'給与：{"{:,}".format(int_input_salary)}円の場合、支給額：{"{:,}".format(pay)}円、税額：{"{:,}".format(tax)}円です。'

        return render_template("output.html", salary = text)

#戻る
@app.route('/input', methods = ['POST'])
def route_input():
    if request.method == 'POST':
        return render_template('input.html')