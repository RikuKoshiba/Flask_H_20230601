from flask_blog import db
from datetime import datetime


class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer)
    user_seq = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    last_edited_at = db.Column(db.DateTime)

    def __init__(self,
                 title=None,
                 text=None,
                 user_id=None,
                 last_edited_at=None):
        self.title = title
        self.text = text
        self.user_id = user_id
        self.created_at = datetime.utcnow()
        self.last_edited_at = last_edited_at

    def __repr__(self):
        return "<Entry id:{} title:{} text:{}>" \
                .format(self.id, self.title, self.text)
