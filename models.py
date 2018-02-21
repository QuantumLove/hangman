from app import db
from sqlalchemy.dialects.postgresql import JSON


class Words(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String)

    def __repr__(self):
        return self.word


class Highscores(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return self.name


class Session(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(JSON)

    def __repr__(self):
        return 'session %d' % self.id