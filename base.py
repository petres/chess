from settings import *
from printer import WithoutColorPrinter, AnsiColorPrinter


class ChessPiece:
    color       = None
    pos         = False
    moved       = False
    ucOffset    = None
    ascii       = None

    def __init__(self, color):
        self.color = color

    def move(self, target):
        pass

    def getPossibleMoves(self):
        pass


class King(ChessPiece):
    ucOffset    = 0
    ascii       = 'K'

class Queen(ChessPiece):
    ucOffset    = 1
    ascii       = 'Q'

class Rook(ChessPiece):
    ucOffset    = 2
    ascii       = 'R'
    moveTypes   = []

class Bishop(ChessPiece):
    ucOffset    = 3
    ascii       = 'B'

class Knight(ChessPiece):
    ucOffset    = 4
    ascii       = 'N'

class Pawn(ChessPiece):
    ucOffset    = 5
    ascii       = 'P'    



class Movements:
    pos =  None
    color = None
    def __init__(self, pos, color = None):
        self.pos = Board.tI(pos)
        self.color = color

    def getSpec(self):
        rStr = "Position: " + Board.tN(self.pos)
        if self.color != None:
            rStr += ", Color: " + self.color
        return rStr

    def getPossibleMoves(self, position, board):
        pass

    def __str__(self):
        rStr = self.__class__.__name__ + "\n";
        rStr += " " + self.getSpec() + "\n";
        rStr += " Possible Moves: " + "\n";
        for group in self.getPossibleMoves():
            rStr += "   - "
            for move in group:
                rStr += Board.tN(move) + " "
            rStr += "\n"
        return rStr

class RookMovements(Movements):
    def getPossibleMoves(self):
        i, j = self.pos
        moveGroups = []

        # UP
        moves = []
        for k in range(j + 1, 8):
            moves.append((i, k))
        moveGroups.append(moves)

        # DOWN
        moves = []
        for k in range(j - 1, -1, -1):
            moves.append((i, k))
        moveGroups.append(moves)

        # RIGHT
        moves = []
        for k in range(i + 1, 8):
            moves.append((k, j))
        moveGroups.append(moves)
            
        # LEFT
        moves = []
        for k in range(i - 1, -1, -1):
            moves.append((k, j))
        moveGroups.append(moves)

        return moveGroups
          


class BishopMovements(Movements):
    def getPossibleMoves(self):
        i, j = self.pos
        moveGroups = []

        # RIGHT UP
        moves = []
        for k in range(0, min(7 - i, 7 - j) ):
            moves.append((i + (k + 1), j + (k + 1)))
        moveGroups.append(moves)

        # LEFT UP
        moves = []
        for k in range(0, min(i, 7 - j) ):
            moves.append((i - (k + 1), j + (k + 1)))
        moveGroups.append(moves)

        # RIGHT DOWN
        moves = []
        for k in range(0, min(7 - i, j)):
            moves.append((i + (k + 1), j - (k + 1)))
        moveGroups.append(moves)
            
        # LEFT DOWN
        moves = []
        for k in range(0, min(i, j)):
            moves.append((i - (k + 1), j - (k + 1)))
        moveGroups.append(moves)

        return moveGroups


class PawnMovements(Movements):
    def getPossibleMoves(self):
        i, j = self.pos
        if self.color is None:
            raise Exception("Pawn Movements need a color")

        start = 1
        direction = 1
        if self.color == C.B:
            start = 6
            direction = -1

        moves = []
        moves.append((i, j + direction))
        if j == start:
            moves.append((i, j + direction*2))

        return [moves]

class KnightMovements(Movements):
    def getPossibleMoves(self):
        i, j = self.pos
        moves = []
        for jump in [(2,1), (2,-1), (-2,1), (-2,-1)]:
            for dir in [1, -1]:
                iii, jjj = jump[::dir]
                ii = i + jjj
                jj = j + iii
                if not ( ii == i and jj == j) and ii >= 0 and ii <= 8 and jj >= 0 and jj <= 8:
                    moves.append((ii, jj))

        return [moves]


class KingMovements(Movements):
    def getPossibleMoves(self):
        i, j = self.pos
        moves = []
        for ii in range(i - 1, i + 2):
            for jj in range(i - 1, i + 2):
                if ii >= 0 and ii <= 8 and jj >= 0 and jj <= 8:
                    moves.append((ii, jj))

        return [moves] 


class Board:
    b = [[None for x in range(8)] for y in range(8)]
    
    def __init__(self):
        if Settings.ansiColors:
            self.printer = AnsiColorPrinter
        else:
            self.printer = WithoutColorPrinter

    def setStartPosition(self):
        for i in range(1, 9):
            self[(i, 2)] = Pawn(C.W)
            self[(i, 7)] = Pawn(C.B)

        for i in [1, 8]:
            self[(i, 1)] = Rook(C.W)
            self[(i, 8)] = Rook(C.B)

        for i in [2, 7]:
            self[(i, 1)] = Knight(C.W)
            self[(i, 8)] = Knight(C.B)

        for i in [3, 6]:
            self[(i, 1)] = Bishop(C.W)
            self[(i, 8)] = Bishop(C.B)

        self['D1'] = King(C.W)
        self['D8'] = King(C.B)

        self['E1'] = Queen(C.W)
        self['E8'] = Queen(C.B)


    def __getitem__(self, key):
        i = self.tI(key)
        return self.b[i[1]][i[0]] 

    def __setitem__(self, key, value):
        i = self.tI(key)
        value.pos  = i
        self.b[i[1]][i[0]] = value

    @staticmethod
    def tI(key):
        if isinstance(key, tuple):
            xL, yL = key
            x = xL - 1
            y = yL - 1
            return (x, y)
        else:
            xL, yL = key
            x = ord(xL.lower()) - 97
            y = int(yL) - 1
            return (x, y)

    @staticmethod
    def tN(pos):
        return chr(97 + pos[0]).upper() + str(pos[1] + 1)

    def __str__(self):
        rStr = self.printer.outputColLabels(True) + "\n"
        for j in range(8)[::-1]:
            rStr += self.printer.outputRowLabel(j + 1, True) 
            for i in range(8):
                cell = self.b[j][i]
                rStr += self.printer.outputCell(cell, (i+j)%2 == 1)
            rStr += self.printer.outputRowLabel(j + 1) + "\n"
        rStr += self.printer.outputColLabels() + "\n"
        return rStr

