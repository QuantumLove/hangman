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
# TODO: Add documentation
# TODO: Refactor score changes into the config file


@app.route('/start', methods=['POST'])
def start_game():
    session['lives'] = 6
    session['score'] = 0
    session['scoreSubmited'] = False

    session.pop('word', None)

    return 'Session Created'


@app.route('/newLevel', methods=['POST'])
def get_level():
    if 'lives' in session and session['lives'] > 0 and 'word' not in session:
        session['guesses'] = []
        session['correct_guesses'] = 0

        if db.session.query(Words).count() == 0:
            return 'There are no available words at the moment!', 200

        # Choose a word
        row = db.session.query(Words).order_by(func.random()).first()

        word = row.word
        spaces = len(row.word)
        category = row.category
        print("Word is " + word + ", spaces are " + str(spaces) + ", and category is " + category)

        session['word'] = list(row.word)
        session['hint'] = row.hint

        resp = jsonify({'spaces': len(session['word']),
                        'category': row.category
                        })
        resp.status_code = 200

        return resp
    else:
        return 'Invalid', 400


@app.route('/hint', methods=['POST'])
def get_hint():
    if 'word' in session and 'hint' in session:
        session['score'] -= 30

        resp = jsonify({'hint': session['hint'], 'score': session['score']})
        resp.status_code = 200
        return resp
    else:
        return 'Invalid', 400


@app.route('/play', methods=['POST'])
def choose_letter():

    data = request.get_json(force=True)

    if 'lives' in session and session['lives'] > 0 and \
            'word' in session and 'letter' in data and \
            data['letter'] not in session['guesses']:

        session['guesses'].append(data['letter'])

        # Check if letter is in the word
        correct = False
        positions = []
        for i in range(len(session['word'])):
            if data['letter'].upper() == session['word'][i].upper():
                correct = True
                session['score'] += 10
                session['correct_guesses'] += 1
                positions.append(i)

        if not correct:
            session['score'] -= 5
            session['lives'] -= 1
            result = 'lost' if session['lives'] <= 0 else 'incorrect'

            resp = jsonify({'result': result,
                            'score': session['score']})

        # Win condition
        elif session['correct_guesses'] == len(session['word']):
            session['score'] += 50
            session.pop('word', None)
            resp = jsonify({'result': 'win',
                            'positions': positions,
                            'score': session['score']})

        # Correct guess
        else:
            resp = jsonify({'result': 'correct',
                            'positions': positions,
                            'score': session['score']})

        session.modified = True
        resp.status_code = 200
        return resp

    else:
        return 'Invalid', 400


@app.route('/highscores', methods=['GET'])
def highscores():
    # Return the top 20 highscores TODO: Make it Json
    scores = db.session.query(Highscores).order_by(desc(Highscores.score)).all()

    resp = jsonify({'scores': [row.to_dict() for row in scores]})
    resp.status_code = 200
    return resp


@app.route('/end', methods=['POST'])
def submit_score():
    data = request.get_json(force=True)

    if 'lives' in session and session['lives'] == 0 and 'score' in session and \
                    'name' in data and not session['scoreSubmited']:

        # Submit the gotten score
        highscore = Highscores(name=data['name'], score=session['score'])
        db.session.add(highscore)
        db.session.commit()

        session['scoreSubmited'] = True

        # Delete scores if there are more than 20
        count = db.session.query(Highscores).count()
        if count > 20:
            records = db.session.query(Highscores).order_by(Highscores.score).limit(count - 20)
            for record in records:
                db.session.delete(record)
            db.session.commit()

        return 'Successfully submitted the score', 200
    else:
        return 'Invalid', 400


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/init', methods=['GET'])
def initialize_db():
    """ Put some initial entries in the database"""

    if db.session.query(Words).count() > 0:
        return 'The database has already been initialized'

    db.session.query(Words).delete()
    db.session.commit()

    words = [
        Words(word='3dhubs', hint='Your go-to service for ordering custom parts online', category='Companies'),
        Words(word='marvin', hint='AKA the depressed Android', category="The Hitchhiker's Guide to the Galaxy"),
        Words(word='print', hint='Now a function, not a statement', category='Python'),
        Words(word='filament', hint='Used for fused deposition modeling', category='Materials'),
        Words(word='order', hint='line, plan, regulation, rule, structure, system, neatness', category='Nouns'),
        Words(word='layer', hint='A person or thing that lays', category='Occupations')
    ]
    for word in words:
        db.session.add(word)
    db.session.commit()

    return 'Number of words in the database ' + str(db.session.query(Words).count())

if __name__ == '__main__':
    app.run()
