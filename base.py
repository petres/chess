from settings import *
from printer import WithoutColorPrinter, AnsiColorPrinter

#######################################################
### Movements
#######################################################

class Movements:
    pos =  None
    color = None
    piece = None

    def __init__(self, pos = None, color = None, piece = None):
        if pos is not None:
            self.pos = Board.tI(pos)
        self.color = color
        self.piece = piece

    def getPos(self):
        if self.piece is not None:
            return self.piece.getPos()
        return self.pos

    def getColor(self):
        if self.piece is not None:
            return self.piece.getColor()
        return self.color

    def getSpec(self):
        rStr = "Position: " + Board.tN(self.getPos())
        if self.color != None:
            rStr += ", Color: " + self.getColor()
        return rStr

    def getPossibleMoves(self):
        pass


    def __str__(self):
        rStr = self.__class__.__name__ + " | " + self.getSpec() + "\n";
        for group in self.getPossibleMoves():
            rStr += "   - "
            for move in group:
                rStr += Board.tN(move) + " "
            rStr += "\n"
        return rStr


class RookMovements(Movements):
    def getPossibleMoves(self):
        i, j = self.getPos()
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
        i, j = self.getPos()
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
        i, j = self.getPos()
        if self.getColor() is None:
            raise Exception("Pawn Movements need a color")

        start = 1
        direction = 1
        if self.getColor() == C.B:
            start = 6
            direction = -1

        moves = []
        moves.append((i, j + direction))
        if j == start:
            moves.append((i, j + direction*2))

        return [moves]


class KnightMovements(Movements):
    def getPossibleMoves(self):
        i, j = self.getPos()
        moves = []
        for jump in [(2,1), (2,-1), (-2,1), (-2,-1)]:
            for dir in [1, -1]:
                iii, jjj = jump[::dir]
                ii = i + jjj
                jj = j + iii
                if not ( ii == i and jj == j) and ii >= 0 and ii <= 7 and jj >= 0 and jj <= 7:
                    moves.append([(ii, jj)])

        return moves


class KingMovements(Movements):
    def getPossibleMoves(self):
        i, j = self.getPos()
        moves = []
        for ii in range(i - 1, i + 2):
            for jj in range(j - 1, j + 2):
                if not (ii == i and jj == j) and  ii >= 0 and ii <= 7 and jj >= 0 and jj <= 7:
                    moves.append([(ii, jj)])

        return moves

#######################################################


#######################################################
### Chess Pieces
#######################################################

class ChessPiece:
    color       = None
    pos         = False
    moved       = False
    ucOffset    = None
    ascii       = None
    moveClasses = []
    moveIns     = []
    board       = None

    def __init__(self, color):
        self.color      = color
        self.moveIns    = []
        for c in self.moveClasses:
            mI = c(piece = self)
            #print(mI.__class__.__name__)
            self.moveIns.append(mI)

    def move(self, t):
        if t in self.getPossibleMoves():
            oldPos = self.pos
            self.board[t] = self
            self.moved = True
            self.board[oldPos] = None
        else:
            print("Not possible")

    def getPos(self):
        return self.pos

    def getColor(self):
        return self.color

    def getPiecePossibleMoves(self):
        t = []
        for ins in self.moveIns:
            t.extend(ins.getPossibleMoves())
        return t

    def getPossibleMoves(self):
        t = []
        for group in self.getPiecePossibleMoves():
            if len(group) == 0:
                continue

            for e in group:
                #print(e, Board.tN(e), self.board[e].__class__.__name__)
                if self.board[e] != None:
                    break
                t.append(e)

        t.extend(self.getAddMoves())
        return t

    def getAddMoves(self):
        return []

    def __str__(self):
        rStr = "-" + self.__class__.__name__ + "\n"
        rStr += "  Position: " + Board.tN(self.pos) + ", Color: " + self.color + "\n"
        rStr += "  Possible Moves: "
        for i, group in enumerate(self.getPossibleMoves()):
            if isinstance(group, list):
                if i == 0:
                    rStr += "\n"
                rStr += "    - "
                for move in group:
                    rStr += Board.tN(move) + " "
                rStr += "\n"
            else:
                rStr += Board.tN(group) + " "
        return rStr


class King(ChessPiece):
    ucOffset    = 0
    ascii       = 'K'
    moveClasses = [KingMovements]

    def move(self, t):
        # Rochade
        if t in self.getAddMoves():
            oldPos = self.pos
            self.board[t] = self
            self.moved = True
            self.board[oldPos] = None
            if self.pos[0] == 1:
                oldPos = (0, self.pos[1])
                self.board[(2, self.pos[1])] = self.board[oldPos]
                self.board[oldPos] = None
            else:
                oldPos = (7, self.pos[1])
                self.board[(4, self.pos[1])] = self.board[oldPos]
                self.board[oldPos] = None    
        else:
            super().move(t)

    def getAddMoves(self):
        # Rochade
        moves = []
        for i in [0, 7]:
            if self.moved == False:
                mP = self.board[(i, self.pos[1])]
                if isinstance(mP, Rook) and mP.getColor() == self.getColor() and mP.moved == False:
                    between = []
                    if i == 0:
                        between = range(1, 3)
                    else:
                        between = range(4, 7)
                    
                    possible = True
                    for ii in between:
                        if self.board[(ii, self.pos[1])] is not None:
                            possible = False
                            break
                    # TODO CHECK CHECK!
                    if possible:
                        if i == 0:
                            move = (1, self.pos[1])
                        else:
                            move = (5, self.pos[1])
                        moves.append(move)

        return moves

class Queen(ChessPiece):
    ucOffset    = 1
    ascii       = 'Q'
    moveClasses = [RookMovements, BishopMovements]

class Rook(ChessPiece):
    ucOffset    = 2
    ascii       = 'R'
    moveClasses = [RookMovements]

class Bishop(ChessPiece):
    ucOffset    = 3
    ascii       = 'B'
    moveClasses = [BishopMovements]

class Knight(ChessPiece):
    ucOffset    = 4
    ascii       = 'N'
    moveClasses = [KnightMovements]

class Pawn(ChessPiece):
    ucOffset    = 5
    ascii       = 'P'
    moveClasses = [PawnMovements]

    def getAddMoves(self):
        moves = []
        i, j = self.getPos()

        direction = 1
        if self.getColor() == C.B:
            direction = -1

        if i != 0 and self.board[i - 1 , j + direction] is not None and self.board[i - 1, j + direction].getColor() != self.getColor():
            moves.append((i - 1, j + direction))

        if j != 7 and self.board[i + 1 , j + direction] is not None and self.board[i + 1, j + direction].getColor() != self.getColor():
            moves.append((i + 1, j + direction))

        # en passant

        return moves

#######################################################


#######################################################
### Board
#######################################################

class Board:
    b = [[None for x in range(8)] for y in range(8)]
    pawnDoubleMove = None
    
    def __init__(self):
        if Settings.ansiColors:
            self.printer = AnsiColorPrinter
        else:
            self.printer = WithoutColorPrinter

    def setStartPosition(self):
        for i in range(8):
            self[(i, 1)] = Pawn(C.W)
            self[(i, 6)] = Pawn(C.B)

        for i in [0, 7]:
            self[(i, 0)] = Rook(C.W)
            self[(i, 7)] = Rook(C.B)

        for i in [1, 6]:
            self[(i, 0)] = Knight(C.W)
            self[(i, 7)] = Knight(C.B)

        for i in [2, 5]:
            self[(i, 0)] = Bishop(C.W)
            self[(i, 7)] = Bishop(C.B)

        self['D1'] = King(C.W)
        self['D8'] = King(C.B)

        self['E1'] = Queen(C.W)
        self['E8'] = Queen(C.B)

    def __getitem__(self, key):
        i = self.tI(key)
        return self.b[i[1]][i[0]] 

    def __setitem__(self, key, value):
        i = self.tI(key)
        if value:
            value.pos       = i
            value.board     = self
        self.b[i[1]][i[0]] = value

    def move(self, oPos, tPos):
        o = self.tI(oPos)
        t = self.tI(tPos)
        
        oP = self[o]
        print("Try to move:", Board.tN(o), "->",Board.tN(t))

        if oP:
            oP.move(t)
        else:
            print("No piece at " + Board.tN(o))

    @staticmethod
    def tI(key):
        if isinstance(key, tuple):
            xL, yL = key
            x = xL
            y = yL
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

#######################################################