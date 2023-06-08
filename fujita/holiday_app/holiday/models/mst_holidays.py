from holiday import db
from datetime import datetime


class Holiday(db.Model):
    __tablename__ = 'holiday_app'
    holi_date = db.Column(db.Date, primary_key=True)
    holi_text = db.Column(db.String(20))

    def __init__(self, holi_date=None, holi_text=None):
        self.holi_date = holi_date
        self.holi_text = holi_text
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Holiday date:{} text:{}>'.format(self.holi_date, self.holi_text)
