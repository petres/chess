class Settings:
    utf8        = True
    ansiColors  = True
    fileName	= "board.txt"
    posFolder	= "positions"

class C:
    class W:
        name        = "White"
        direction   = 1
        pawnStart   = 1
        pawnLast    = 7
    class B:
        name        = "Black"
        direction   = -1
        pawnStart   = 6
        pawnLast    = 0


C.W.O = C.B
C.B.O = C.W