from settings import *
from base import *

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

        rStr += sign + ' |'

        return rStr

    @staticmethod
    def getSignForPiece(p, utf8 = Settings.utf8):
        if utf8:
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
