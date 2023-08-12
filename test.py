from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def test_gen_board(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            """test status code"""
            self.assertEqual(res.status_code, 200)

            """test html response"""
            self.assertIn('<th colspan="5">Boggle!</th>', html)
            with client.session_transaction() as change_session:
                change_session['record'] = 80
            client.get('/')
            """check session"""
            self.assertEqual(session['record'], 80)

    def test_check_guess(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['boggle_board'] = ['D', 'O', 'G', "G", "Y"]
            res = client.get('/guess?word=dog')
            """check peram and response"""
            self.assertEqual(res.json['result'], 'ok')

    def test_update_status(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['record'] = 80
                change_session['times_played'] = 1
            res = client.post('/stats', json={'score': 100, 'times_played': 1})
            self.assertEqual(res.json['new_record'], True)
            with client.session_transaction() as session:
                self.assertEqual(session['record'], 100)
                self.assertEqual(session['times_played'], 2)
    
    # TODO -- write tests for every view function / feature!