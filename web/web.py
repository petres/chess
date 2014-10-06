#!/usr/bin/python3
from flask import Flask
from flask import render_template
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import simplejson as sj


from base import *

b = Board()
b.setStartPosition();

app = Flask(__name__)

@app.route('/')
def base():
	return render_template('base.html')

@app.route('/getBoardInfo')
def getBoardInfo():
	return _getBoardInfo()

@app.route('/move/<origin>/<target>')
def move(origin, target):
	b.move(origin, target)
	return _getBoardInfo()


def _getBoardInfo():
	info = {}
	for i in range(8):
		for j in range(8):
			piece = b[(i,j)]
			if piece:
				possibleMoves = list(map(b.tN, piece.getPossibleMoves()))
				print(possibleMoves)
				info[b.tN((i,j))] = {	'color': piece.color.name.lower(), 
										'piece': piece.__class__.__name__.lower(), 
										'possibleMoves': possibleMoves}
			else:
				info[b.tN((i,j))] = None 
	return sj.dumps(info)

if __name__ == '__main__':
    app.run(debug=True)