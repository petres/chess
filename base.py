from settings import *
from printer import WithoutColorPrinter, AnsiColorPrinter

import os, sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))
#######################################################
### Movements
#######################################################
# Todo Refactoring, this classes are nearly useless

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

        start = self.getColor().pawnStart
        direction = self.getColor().direction

        moves = []
        if j != self.getColor().pawnLast:
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
    pos         = None
    moved       = False
    ucOffset    = None
    ascii       = None
    moveClasses = []
    moveIns     = []
    board       = None


    def __init__(self, color):
        self.color      = color
        self.moveIns    = []
        self.pos        = None
        for c in self.moveClasses:
            mI = c(piece = self)
            #print(mI.__class__.__name__)
            self.moveIns.append(mI)


    def move(self, t):
        if t in self.getPossibleMoves():
            self.board[self.pos] = None
            self.board[t] = self
            self.moved = True
            self.board.pawnDoubleMove = None
            return True
        else:
            print("Not possible")
            return False


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
            for e in group:
                tPiece = self.board[e]
                if tPiece != None:
                    if tPiece.color != self.color and not isinstance(self, Pawn):
                        t.append(e)
                    break
                t.append(e)

        t.extend(self.getAddMoves())

        r = []
        for m in t:
            if not self.board.isCheckAfterMove(self, m):
                r.append(m)  

        return r

    def getCaptureMoves(self):
        return self.getPiecePossibleMoves()

    def getAddMoves(self):
        return []


    def __str__(self):
        rStr = "- " + self.__class__.__name__ + ", Color: " + self.color.name + "\n"
        if self.pos:
            rStr += "  Position: " + Board.tN(self.pos) + "\n"
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
        if t in self.getRochadeMoves() and t in self.getPossibleMoves():
            self.board[self.pos] = None
            self.board[t] = self
            self.moved = True
            if self.pos[0] == 1:
                rookOldPos = (0, self.pos[1])
                rookNewPos = (2, self.pos[1])
            else:
                rookOldPos = (7, self.pos[1])
                rookNewPos = (4, self.pos[1])
            rook = self.board[rookOldPos]
            self.board[rookOldPos] = None
            self.board[rookNewPos] = rook
            self.board.pawnDoubleMove = None
            return True  
        else:
            return super().move(t)


    def getRochadeMoves(self):
        moves = []
        for i in [0, 7]:
            if self.moved == False:
                mP = self.board[(i, self.pos[1])]
                if isinstance(mP, Rook) and mP.getColor() == self.color and mP.moved == False:
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

                    if possible:
                        if self.board.isFieldThreaten(self.pos, self.color.O):
                            possible = False

                    if possible:
                        for ii in between:
                            if self.board.isFieldThreaten((ii, self.pos[1]), self.color.O):
                                possible = False
                                break

                    if possible:
                        if i == 0:
                            move = (1, self.pos[1])
                        else:
                            move = (5, self.pos[1])
                        moves.append(move)
        return moves

    def getAddMoves(self):
        return self.getRochadeMoves()


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


    def move(self, t):
        if t in self.getEnPassantMoves() and t in self.getPossibleMoves():
            oldPos = self.pos
            self.board[self.pos] = None
            self.board[t] = self
            self.moved = True
            self.board[(t[0], oldPos[1])] = None
            self.board.pawnDoubleMove = None
            return True
        elif abs(t[1] - self.pos[1]) == 2:
            # Setting for possibility of en passent
            if super().move(t):
                self.board.pawnDoubleMove = self.pos
                return True
            else:
                return False
        elif (t[1] == 7 and self.color == C.W) or (t[1] == 0 and self.color == C.B):
            if t in self.getPossibleMoves():
                self.board[self.pos] = None
                self.board[t] = Queen(self.color)
                self.moved = True
                self.board.pawnDoubleMove = None
                return True
            else:
                return False
        else:
            return super().move(t)


    def getCaptureMoves(self, potential = True):
        moves = []
        i, j = self.pos
        direction = self.color.direction

        if j == self.color.pawnLast:
            return []

        if potential: 
            if i != 0:
                moves.append([(i - 1, j + direction)])
            
            if i != 7:
                moves.append([(i + 1, j + direction)])
        else:     
            if i != 0 and self.board[i - 1 , j + direction] is not None and self.board[i - 1, j + direction].getColor() != self.color:
                moves.append((i - 1, j + direction))
            
            if i != 7 and self.board[i + 1 , j + direction] is not None and self.board[i + 1, j + direction].getColor() != self.color:
                moves.append((i + 1, j + direction))

        return moves


    def getEnPassantMoves(self):
        if self.board.pawnDoubleMove is not None:
            i, j = self.getPos()
            if j == self.board.pawnDoubleMove[1] and abs(i - self.board.pawnDoubleMove[0]) == 1 and self.board[self.board.pawnDoubleMove].getColor() != self.getColor(): 
                direction = self.getColor().direction
                return [(self.board.pawnDoubleMove[0], self.board.pawnDoubleMove[1] + direction)]

        return []


    def getAddMoves(self):
        return self.getCaptureMoves(potential = False) + self.getEnPassantMoves()

#######################################################


class GameStatus:
    NotFinished = 0
    CheckMate   = 1
    StaleMate   = 2



#######################################################
### Board
#######################################################

class Board:
    def __init__(self):
        self.pieces = {}
        self.pieces[C.B] = []
        self.pieces[C.W] = []

        self.king = {}
        self.king[C.B] = None
        self.king[C.W] = None

        self.turnOf = C.W

        self.b = [[{'p': None, 't': {C.B: [], C.W:[]}} for x in range(8)] for y in range(8)]
        self.pawnDoubleMove = None

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

        self.analyse()


    def fieldInfo(self, key):
        i, j = self.tI(key)
        return self.b[j][i]


    def printFieldInfo(self, key):
        fieldInfo = self.fieldInfo(key)['t']
        for c in fieldInfo:
            if len(fieldInfo[c]) > 0:
                print(c.name)
            for p in fieldInfo[c]:
                print(" -", p.__class__.__name__, self.tN(p.pos))


    def __getitem__(self, key):
        i, j = self.tI(key)
        return self.b[j][i]['p']


    def __setitem__(self, key, piece):
        i, j = self.tI(key)
        cPiece = self[i,j]

        if cPiece is not None:
            cPiece.pos = None
            self.pieces[cPiece.color].remove(cPiece)

        if piece:
            if piece.pos is None:
                self.pieces[piece.color].append(piece)
            piece.pos       = (i, j)
            if isinstance(piece, King):
                self.king[piece.color] = piece.pos
            piece.board     = self

        self.b[j][i]['p'] = piece


    def move(self, oPos, tPos):
        o = self.tI(oPos)
        t = self.tI(tPos)
        
        oP = self[o]
        print("Try to move:", Board.tN(o), "->",Board.tN(t))

        if oP:
            if oP.move(t):
                self.analyse()
                return True
        else:
            print("No piece at " + Board.tN(o))

        return False


    def analyse(self):
        # clear info
        for i in range(8):
            for j in range(8):
                self.fieldInfo((i,j))['t'][C.W] = []
                self.fieldInfo((i,j))['t'][C.B] = []

        for color in [C.W, C.B]:
            for piece in list(self.pieces[color]):
                for fieldGroup in piece.getCaptureMoves():
                    for field in fieldGroup:
                        #print(piece.__class__.__name__, self.tN(field))
                        fieldInfo = self.fieldInfo(field)
                        fieldInfo['t'][piece.color].append(piece)
                        if fieldInfo['p'] != None:
                            break
                        


    def getPossibleMoves(self, color):
        pm = {}
        # list is changing therefore coping
        for piece in list(self.pieces[color]):
            ppm = piece.getPossibleMoves()
            if len(ppm) > 0:
                pm[piece] = ppm
        return pm


    def isFieldThreaten(self, field, color):
        return len(self.fieldInfo(field)['t'][color]) > 0


    def getStatus(self, color):
        if len(self.getPossibleMoves(color)) == 0:
            if self.isCheck(color):
                return GameStatus.CheckMate
            else:
                return GameStatus.StaleMate
        else:
            return GameStatus.NotFinished


    def isCheck(self, color):
        return self.isFieldThreaten(self.king[color], color.O)


    def isCheckAfterMove(self, piece, t, color = None):
        if color is None:
            color = piece.color

        sPos = piece.pos
        tFig = self[t]

        self[sPos] = None
        self[t] = piece
        self.analyse()
        
        r = self.isCheck(color)

        self[t] = tFig
        self[sPos] = piece
        self.analyse()
        return r


    def printPossibleMoves(self, color):
        pm = self.getPossibleMoves(color)
        print("Possible Moves:")
        for p in pm:
            print(p.__class__.__name__, Board.tN(p.pos), "->", end=" ")
            for j in pm[p]:
                print(Board.tN(j), end=" ")
            print()


    @staticmethod
    def tI(key):
        if isinstance(key, tuple):
            return key
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
                cell = self[i,j]
                rStr += self.printer.outputCell(cell, (i+j)%2 == 1)
            rStr += self.printer.outputRowLabel(j + 1) + "\n"
        rStr += self.printer.outputColLabels() + "\n"
        return rStr


    def writeFile(self, fileName = Settings.fileName):
        strRep = ""
        printer = WithoutColorPrinter
        for j in range(8)[::-1]:
            for i in range(8):
                piece = self[i,j]
                s = " "
                if piece:
                    s = printer.getSignForPiece(piece, False)
                strRep += s
            strRep += "\n"
        
        with open(os.path.join(Settings.posFolder, fileName), 'w') as f:
            f.write(strRep)


    @staticmethod
    def readFile(fileName = Settings.fileName):
        b = Board()
        with open(os.path.join(Settings.posFolder, fileName), 'r') as f:
            content = f.read()

        asciiToPiece = {
            "P": Pawn,
            "R": Rook,
            "K": King,
            "N": Knight,
            "B": Bishop,
            "Q": Queen
        }

        for i in range(8):
            for j in range(8):
                value = content[j + i*(8+1)]
                if value != " ":
                    color = C.B
                    if value.isupper():
                        color = C.W
                    pieceLetter = value.upper()

                    b[j,7-i] = asciiToPiece[pieceLetter](color)

        b.analyse()
        return b


#######################################################