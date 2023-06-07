from flask import request, redirect, url_for, render_template, flash, session
from holiday import app
from holiday import db
from holiday.models.mst_holiday import Holiday

@app.route('/list', methods=['GET', 'POST'])
def m_list():
    if request.method == 'POST':
        holidaies = Holiday.query.order_by(Holiday.holi_date.desc()).all()
        return render_template('list.html', holidaies=holidaies)
        
