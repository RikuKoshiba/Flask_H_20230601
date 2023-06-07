from flask import request, redirect, url_for, render_template, flash, session
from diary import app

@app.route('/')
def input():
    return render_template('/index.html')