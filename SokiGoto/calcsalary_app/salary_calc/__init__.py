from flask import Flask
from datetime import timedelta
import secrets

app = Flask(__name__)
app.config.from_object("salary_calc.config")
app.config["SECRET_KEY"] = secrets.token_hex()
app.permanent_session_lifetime = \
    timedelta(minutes=app.config["SESSION_TIME_MIN"])


import salary_calc.views
