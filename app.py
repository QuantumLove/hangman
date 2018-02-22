import os
from flask import Flask, render_template, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, desc

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

# TODO: App cannot return server info on 500


@app.route('/start', methods=['POST'])
def start_game():
    session['lives'] = 6
    session['score'] = 0
    session.pop('word', None)
    return 'Session created'


@app.route('/newLevel', methods=['POST'])
def get_level():
    if 'lives' in session and 'word' not in session:
        if session['lives'] > 0:
            # Choose a word
            row = db.session.query(Words).order_by(func.rand()).first

            # Warning: Assumes there are words in the database

            print("Word is %s, spaces are %d, and category is %s".format(row.word, len(row.word), row.category))

            session['word'] = row.word
            session['hint'] = row.hint

            return row
    else:
        return 'Invalid'


@app.route('/hint', methods=['POST'])
def get_hint():
    if 'word' in session and 'hint' in session:
        session['score'] -= 30
        return session['hint']
    else:
        return 'Invalid'


@app.route('/play', methods=['POST'])
def choose_letter():

    data = request.get_json(force=True)
    if 'lives' in session and 'word' in session and 'letter' in data:
        if session['lives'] > 0:
            pass
            # Check if letter is valid

            # TODO: Make response JSON
            # Return the letter position(s) or a big fat NO (remaining lives)
            # Also Return the score

    else:
        return 'Invalid'


@app.route('/highscores', methods=['GET'])
def highscores():
    # Return the top 20 highscores TODO: Make it Json
    return db.session.query(Highscores).order_by(desc(Highscores.score))


@app.route('/end', methods=['POST'])
def submit_score():
    data = request.get_json(force=True)

    if 'score' in session and 'name' in data:

        # Submit the gotten score
        highscore = Highscores(name=data['name'], score=session['score'])
        db.session.add(highscore)
        db.session.commit()

        # Delete scores if there are more than 20
        count = db.session.query(Highscores).count()
        if count > 20:
            records = db.session.query(Highscores).order_by(Highscores.score).limit(count - 20)
            for record in records:
                db.session.delete(record)
            db.session.commit()

        return 'Successfully submitted the score'
    else:
        return 'Invalid'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Put some initial entries in the database
# @app.route('/init', methods=['GET'])
# def initialize_db():
#
#     db.session.query(Words).delete()
#     db.session.commit()
#
#     words = [
#         Words(word='3dhubs', hint='Your go-to service for ordering custom parts online', category='Companies'),
#         Words(word='marvin', hint='Aka the paranoid Android', category="The Hitchhiker's Guide to the Galaxy"),
#         Words(word='print', hint='Now a function, not a statement', category='Python'),
#         Words(word='filament', hint='Used for fused deposition modeling', category='Materials'),
#         Words(word='order', hint='line, plan, regulation, rule, structure, system, neatness', category='Nouns'),
#         Words(word='layer', hint='A person or thing that lays', category='Occupations')
#     ]
#     for word in words:
#         db.session.add(word)
#     db.session.commit()
#
#     return 'Number of words ' + str(db.session.query(Words).count())

if __name__ == '__main__':
    app.run()
