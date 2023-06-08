from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("login_hack.config")

# db = SQLAlchemy(app)

from login_hack.views import views
