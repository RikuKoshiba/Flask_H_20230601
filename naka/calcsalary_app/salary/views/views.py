from flask import request, redirect, url_for, render_template, flash, session
from salary import app

@app.route('/')
def input():
    # if request.method == 'POST':
    #     return 
    return render_template("input.html")   