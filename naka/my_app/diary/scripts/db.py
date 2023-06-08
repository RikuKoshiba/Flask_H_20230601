from flask_script import Command
from diary import db
from diary.models.diary import Diary

class InitDB(Command):
    "create database"

    def run(self):
        db.create_all()
