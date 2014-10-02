class Settings:
    utf8        = True
    ansiColors  = True
    fileName	= "board.txt"
    posFolder	= "positions"

class C:
    class W:
    	name 		= "White"
    	direction 	= 1
    class B:
    	name 		= "Black"
    	direction 	= -1


C.W.O = C.B
C.B.O = C.W