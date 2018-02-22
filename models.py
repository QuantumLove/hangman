from app import db
from sqlalchemy.dialects.postgresql import JSON


class Words(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String)
    category = db.Column(db.String, nullable=False)
    hint = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.word


class Highscores(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer)

    def __repr__(self):
        return self.name


# Sessions are not being managed by the database
# class Session(db.Model):
#
#     id = db.Column(db.Integer, primary_key=True)
#     sessionToken = db.Column(db.String)
#     session = db.Column(JSON)
#     ...
#
#     def __repr__(self):
#         return 'session %d' % self.id