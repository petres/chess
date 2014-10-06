#!/usr/bin/python3
from flask import Flask
from flask import render_template
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "player"))

from base import *
from settings import *

from ki import *


import simplejson as sj


from base import *

b = Board()
b.setStartPosition();

p = KillBest(C.B)


app = Flask(__name__)

@app.route('/')
def base():
	return render_template('base.html')

@app.route('/getBoardInfo')
def getBoardInfo():
	return _getBoardInfo()

@app.route('/restart')
def restart():
	global b
	b = Board()
	b.setStartPosition();
	return _getBoardInfo()

@app.route('/move/<origin>/<target>')
def move(origin, target):
	# HUMAN MOVE
	b.move(origin, target)

	if b.getStatus(b.turnOf) == GameStatus.NotFinished:
		# COMPUER
		piecePos, toPos = p.move(b)
		b.move(piecePos, toPos)

	return _getBoardInfo()


def _getBoardInfo():
	info = {	'turnOf': 			b.turnOf.name.lower(),
			 	'check':			b.isCheck(b.turnOf),
			 	'over':				len(b.getPossibleMoves(b.turnOf)) == 0 }
	
	if len(b.history) > 0:
		info['lastMove'] = list(map(b.tN, b.history[-1]))

	info['board'] = {}
	for i in range(8):
		for j in range(8):
			piece = b[(i,j)]
			if piece:
				possibleMoves = list(map(b.tN, piece.getPossibleMoves()))
				info['board'][b.tN((i,j))] = {	'color': 	piece.color.name.lower(), 
												'piece': 	piece.__class__.__name__.lower(), 
												'possibleMoves': possibleMoves}
			else:
				info['board'][b.tN((i,j))] = None 
	return sj.dumps(info)

if __name__ == '__main__':
    app.run(debug=True)