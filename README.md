chess
=====

A simple chess engine written in python3. You can play on the terminal or on a web interface (online: http://chess.pre.wiwiwi.at). 

The web interface has two dependecies: 
* [flask](http://flask.pocoo.org/) | microframework, webserver
* [simplejson](http://simplejson.readthedocs.org/) | Writing/Reading JSON

Till now three different KIs are implemented:
* **PureRandom**

  The simplest one. Does randomly draw a move from all possible moves.
  
  
* **KillBill**

  Also a quite simple KI. Captures if possible, if not draw a random move.
  
  
* **KillBest**

  Capture if opposite piece has lower value or isn't guarded. Check if possible (only on non guarded fields). Do randomly draw a move.
