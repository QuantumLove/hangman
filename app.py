import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *


@app.route('/start', methods=['POST'])
def start_game():
    pass
    # Create a session


@app.route('/newLevel', methods=['POST'])
def get_level():

    data = request.get_json(force=True)

    # Choose a word

    # Return the spaces and the session variables


@app.route('/play', methods=['POST'])
def choose_letter():

    data = request.get_json(force=True)

    # Check if letter is valid

    # Return the letter position or a big fat NO (remaining lives)
    # Also Return the score


@app.route('/highscores', methods=['GET'])
def highscores():
    pass
    # Return the top 20 highscores


@app.route('/end', methods=['POST'])
def submit_score():

    data = request.get_json(force=True)

    # Check if session is valid

    # Submit the score gotten

    # Deliver the Highscore table back to the user


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
