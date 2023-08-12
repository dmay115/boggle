from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "boggle"

boggle_game = Boggle()

@app.route('/')
def gen_board():
    """set up for board state"""
    record = session.get("record", 0)
    times_played = session.get("times_played", 0)
    session['boggle_board'] = boggle_game.make_board()
    return render_template('board.html', times_played=times_played, record=record)

@app.route('/guess')
def check_guess():
    """checks user guess against dictionary"""
    word = request.args["word"]
    board = session["boggle_board"]
    res = boggle_game.check_valid_word(board, word)
    return jsonify({'result': res})

@app.route('/stats', methods=["POST"])
def update_stats():
    """sets score record/times played and returns response for highscore"""
    score = request.json["score"]
    record = session.get("record", 0)
    new_record = False
    times_played = session.get("times_played", 0)
    session['times_played'] = times_played + 1
    if (score > record):
        session['record'] = score
        new_record = True
    return jsonify({"new_record": new_record})