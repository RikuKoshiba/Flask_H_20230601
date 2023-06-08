from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('diary.config')

db = SQLAlchemy(app)

from diary.views import views
