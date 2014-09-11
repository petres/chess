#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Settings:
    utf8        = False
    ansiColors  = True


class WithoutColorPrinter:
    div  = "   ---------------------------------   " 
    @staticmethod
    def outputColLabels(first = False):
        rStr = "     a   b   c   d   e   f   g   h     " + '\n'
        
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
            if p['c'] == C.W:
                code = 0x265A
            code += p['p']['ucOffset']
            return str(chr(code))
        else:
            if p['c'] == C.B:
                return p['p']['ascii'].lower()
            else:
                return p['p']['ascii'].upper()


class AnsiColorPrinter(WithoutColorPrinter):
    WHITE_BACK = '\033[1;40m'
    BLACK_BACK = '\033[1;47m'

    WHITE_FORE = '\033[1;34m'
    BLACK_FORE = '\033[1;31m'

    ENDC  = '\033[0m'

    @staticmethod
    def outputColLabels(first = False):
        return "     a  b  c  d  e  f  g  h     " 

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
            if cell['c'] == C.B:
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

    def __getitem__(self, key):
        i = self.tI(key)
        return self.b[i[1]][i[0]] 

    def __setitem__(self, key, value):
        i = self.tI(key)
        self.b[i[1]][i[0]] = value

    def tI(self, key):
        if len(key) > 2:
            pass
        else:
            xL, yL = key
            x = ord(xL.lower()) - 97
            y = int(yL) - 1
            return (x, y)

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

class P:
    K = { 'ucOffset': 0,
          'ascii':   'K'}
    Q = { 'ucOffset': 1,
          'ascii':   'Q'}
    R = { 'ucOffset': 2,
          'ascii':   'R'}
    B = { 'ucOffset': 3,
          'ascii':   'B'}
    N = { 'ucOffset': 4,
          'ascii':   'N'}
    P = { 'ucOffset': 5,
          'ascii':   'P'}


b = Board()

b['E7'] = {'p': P.K, 'c': C.B}
b['E8'] = {'p': P.Q, 'c': C.B}
b['C4'] = {'p': P.R, 'c': C.W}
b['D4'] = {'p': P.B, 'c': C.W}
print(b['A1'])

print(b)