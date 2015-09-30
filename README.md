## Chess Engine

A simple chess engine written in python3. You can play on the terminal or on a [web interface](http://chess.abteil.org/). The chess engine is quite complete. Still missing are: Fifty-move rule and the threefold repetition. 

### Web Interface

The web interface has two dependecies: 
* [flask](http://flask.pocoo.org/) | Micro web framework, used also as webserver
* [simplejson](http://simplejson.readthedocs.org/) | Writing/Reading JSON

Calling `web/web.py` starts the webserver with the chess engine on port 5000.

## AI 

Till now three different AIs are implemented (https://github.com/petres/chess/blob/master/player/ki.py):
* **PureRandom**

  The simplest one. Does randomly draw a move from all possible moves.
  
  
* **KillBill**

  Also a quite simple KI. Captures if possible, if not draw a random move.
  
  
* **KillBest**

  Capture if opposite piece has lower value or isn't guarded. Check if possible (only on non guarded fields). Do randomly draw a move.
