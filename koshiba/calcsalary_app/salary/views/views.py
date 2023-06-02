from flask import request, redirect, url_for, render_template, flash, session
from salary import app
from decimal import Decimal, ROUND_HALF_UP

@app.route('/')
def m_input():
    return render_template('input.html')

@app.route('/output', methods=['GET', 'POST'])
def m_output():
    if request.method == 'POST':
        #給与で税率変更
        allowance = int(request.form["input_salary"])
        if allowance > 1000000:
            tax = (allowance - 1000000) * 0.2 + 1000000 * 0.1
        else:
            tax = allowance * 0.1

        # 税率から支給額算出
        tax = Decimal(str(tax)).quantize(Decimal("0"),rounding=ROUND_HALF_UP)
        salary = allowance - tax

        # output.htmlに結果を渡す、遷移
        return render_template('output.html', allowance=allowance, tax=tax, salary=salary)


# @app.route('/logout')
# def logout():
#     # session.pop('logged_in', None)
#     flash('ログアウトしました')
#     return redirect(url_for('show_entries'))

