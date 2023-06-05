from flask import request, redirect, url_for, render_template, flash, session
from holiday import app
from holiday import db
from holiday.models.mst_holiday import Holiday


@app.route('/result', methods=['GET', 'POST'])
def m_result():
    if request.method == 'POST':
        return render_template('result.html')

