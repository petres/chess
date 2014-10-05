#!/usr/bin/python3
from flask import Flask
from flask import render_template

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import simpeljson

from player import Player

from base import *

app = Flask(__name__)

@app.route('/')
def show():
	return render_template('base.html')

@app.route('/update')
def show():
	return render_template('base.html')

if __name__ == '__main__':
    app.run()