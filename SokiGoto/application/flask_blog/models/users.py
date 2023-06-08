from flask_blog import db


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    loginid = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(120))
    username = db.Column(db.String(20))
    image_path = db.Column(db.String(70))

    def __init__(self, loginid=None, password=None):
        self.loginid = loginid
        self.password = password
        self.username = loginid
        self.image_path = None

    def __repr__(self):
        return "<Users id:{} username:{}>" \
                .format(self.id, self.username)
