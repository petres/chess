#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Settings:
    utf8        = True
    ansiColors  = True


class WithoutColorPrinter:
    div  = "   ---------------------------------   " 
    @staticmethod
    def outputColLabels(first = False):
        rStr = "     A   B   C   D   E   F   G   H     " + '\n'
        
        if first:
             rStr += WithoutColorPrinter.div

        return rStr
        # else:
        #     return div + rStr

    @staticmethod
    def outputRowLabel(j, first = False):
        rStr = " " + str(j) 
        if first:
            rStr += " |"  
        else:
            rStr += '\n' + WithoutColorPrinter.div 
        return rStr

    @staticmethod
    def outputCell(cell, white):
        rStr = ' '
        if cell is None:
            sign = ' '
        else:
            sign = WithoutColorPrinter.getSignForPiece(cell)

        print(sign)
        rStr += sign + ' |'

        return rStr

    @staticmethod
    def getSignForPiece(p):
        if Settings.utf8:
            code = 0x2654
            if p.color == C.W:
                code = 0x265A
            code += p.ucOffset
            return str(chr(code))
        else:
            if p.color == C.B:
                return p.ascii.lower()
            else:
                return p.ascii.upper()


class AnsiColorPrinter(WithoutColorPrinter):
    WHITE_BACK = '\033[1;40m'
    BLACK_BACK = '\033[1;47m'

    WHITE_FORE = '\033[1;34m'
    BLACK_FORE = '\033[1;31m'

    ENDC  = '\033[0m'

    @staticmethod
    def outputColLabels(first = False):
        return "    A  B  C  D  E  F  G  H     " 

    @staticmethod
    def outputRowLabel(j, first = False):
        return " " + str(j) + " " 

    @staticmethod
    def outputCell(cell, white):
        ansiBack = AnsiColorPrinter.BLACK_BACK
        ansiFore = AnsiColorPrinter.WHITE_FORE

        if white:
            ansiBack = AnsiColorPrinter.WHITE_BACK

        if cell is None:
            sign = ' '
        else:
            sign = WithoutColorPrinter.getSignForPiece(cell)
            if cell.color == C.B:
                ansiFore = AnsiColorPrinter.BLACK_FORE

   
        return ansiBack + ansiFore + ' ' + sign + ' ' + AnsiColorPrinter.ENDC

    # WHITE = '\033[97;100m'
    # BLACK = '\033[90;107m'


class Board:
    b = [[None for x in range(8)] for y in range(8)]
    
    def __init__(self):
        if Settings.ansiColors:
            self.printer = AnsiColorPrinter
        else:
            self.printer = WithoutColorPrinter

    def setStartPosition(self):
        for i in range(1, 9):
            b[(i, 2)] = Pawn(C.W)
            b[(i, 7)] = Pawn(C.B)

        for i in [1, 8]:
            b[(i, 1)] = Rook(C.W)
            b[(i, 8)] = Rook(C.B)

        for i in [2, 7]:
            b[(i, 1)] = Knight(C.W)
            b[(i, 8)] = Knight(C.B)

        for i in [3, 6]:
            b[(i, 1)] = Bishop(C.W)
            b[(i, 8)] = Bishop(C.B)

        b['D1'] = King(C.W)
        b['D8'] = King(C.B)

        b['E1'] = Queen(C.W)
        b['E8'] = Queen(C.B)


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



class C:
    W = 0
    B = 1




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

    def __init__(self, pos):
        self.pos = Board.tI(pos)


    def getPossibleMoves(self, position, board):
        pass

    def __str__(self):
        rStr = "Position " + Board.tN(self.pos) + "\n";
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
    pass

class PawnMovements(Movements):
    pass

class KnightMovements(Movements):
    def getPossibleMoves(self):
        i, j = self.pos
        moves = []
        for jump in [(2,1), (2,-1), (-2,1), (-2,-1)]:
            iii, jjj = jump
            ii = i + iii
            jj = j + jjj
            if not ( ii == i and jj == j) and ii >= 0 and ii <= 8 and jj >= 0 and jj <= 8:
                moves.append((ii, jj))
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

class Player:
    def pleaseMove(self, board):
        # calculate possibiliees
        # calculate for every pos. the value
        # return best move
        pass

r = RookMovements('C4')
print(r)

r = KingMovements('C4')
print(r)

r = KnightMovements('C4')
print(r)

b = Board()

b.setStartPosition();
b['E7'] = King(C.B)
b['D7'] = King(C.W)
# b['E8'] = {'p': Queen, 'c': C.B}
# b['C4'] = {'p': Rock, 'c': C.W}
# b['D4'] = {'p': Bishop, 'c': C.W}

# b[(1, 3)] = {'p': P.P, 'c': C.W}

print(b['A1'])

print(b)

print(Board.tI('A1'))