from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config.from_object("holiday.config")
app.config["SECRET_KEY"] = secrets.token_hex()

db = SQLAlchemy(app)
from holiday.views import input, list, maintenance_date
