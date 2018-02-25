import unittest
from app import create_app
from models import *
import json


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config.from_object('config.TestingConfig')
        self.client = self.app.test_client

        with self.app.app_context():
            db.create_all()

            # Add dummy word
            word = Words(word='3dhubs', hint='Your go-to service for ordering custom parts online', category='Companies')
            db.session.add(word)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def test_database_has_one_entry(self):
        with self.app.app_context():
            self.assertEqual(db.session.query(Words).count(), 1)

    def test_game_can_be_started(self):
        with self.client() as c:
            res = c.post('/start')
            self.assertEqual(res.status_code, 200)

            with c.session_transaction() as session:
                assert 'lives' in session and session['lives'] == 6

    def test_level_can_be_gotten(self):
        with self.client() as c:
            res = c.post('/start')
            self.assertEqual(res.status_code, 200)

            res = c.post('/newLevel')
            self.assertEqual(res.status_code, 200)

            data = json.loads(res.data.decode('utf-8'))

            self.assertEqual(data['spaces'], 6)
            self.assertEqual(data['category'], 'Companies')

    def test_letters_can_be_chosen(self):
        with self.client() as c:
            res = c.post('/start')
            self.assertEqual(res.status_code, 200)

            res = c.post('/newLevel')
            self.assertEqual(res.status_code, 200)

            with c.session_transaction() as session:
                session['word'] = 'foo'

            # Existing letter
            res = c.post('/play', data=json.dumps({'letter': 'f'}))
            print(res.data)
            self.assertEqual(res.status_code, 200)

            print(str(res.data))  # TODO Validate that the right data is in the response (correct)

            # Non existing letter
            res = c.post('/play', data=json.dumps({'letter': 'a'}))
            self.assertEqual(res.status_code, 200)

            print(str(res.data))  # TODO Validate that the right data is in the response (incorrect)


if __name__ == '__main__':
    unittest.main()
