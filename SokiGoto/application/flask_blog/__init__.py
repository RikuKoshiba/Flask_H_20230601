from flask import Flask
from datetime import timedelta
import secrets
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("flask_blog.config")
app.config["SECRET_KEY"] = secrets.token_hex()
app.permanent_session_lifetime = \
    timedelta(minutes=app.config["SESSION_TIME_MIN"])

UPLOAD_FOLDER = './flask_brog/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
from flask_blog.views import views, entries
