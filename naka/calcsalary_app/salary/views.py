from flask import request, redirect, url_for, render_template, flash, session
from salary import app

@app.route('/')
def show_entires():
    return render_template('input.html')
