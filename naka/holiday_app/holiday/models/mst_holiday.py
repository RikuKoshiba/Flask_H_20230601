#データベース定義

from flask_script import Command
from holiday import db
from datetime import datetime

class Holiday(db.Model):
    __tablename__ = 'holiday'
    holi_date = db.Column(db.DateTime, unique = True) 
    holi_text = db.Column(db.String(40))

    def __init__(self, holi_date= None, holi_text = None):
        self.tiholi_datetle = holi_date
        self.holi_text = holi_text

    def __repr__(self):
        return '<Holiday holi_date:{} holi_text:{}>'.format(self.holi_date, self.holi_text)