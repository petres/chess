class Settings:
    utf8        = True
    ansiColors  = True
    fileName	= "board.txt"
    posFolder	= "positions"

class C:
    class W:
        name        = "White"
        ascii       = 'W'
        direction   = 1
        pawnStart   = 1
        pawnLast    = 7
    class B:
        name        = "Black"
        ascii       = 'B'
        direction   = -1
        pawnStart   = 6
        pawnLast    = 0

    def getFromSign(sign):
        if sign == C.W.ascii:
            return C.W
        elif sign == C.B.ascii:
            return C.B



C.W.O = C.B
C.B.O = C.W