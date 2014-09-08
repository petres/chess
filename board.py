 
class WithoutColorPrinter:
    @staticmethod
    def output(b, (i, j)):
        white = ((i+j)%2 == 1)
        cell = b[i][j]
        if cell is None:
            sign = ' '
        else:
            sign = cell['p']
        return ' ' + sign + ' '

class AnsiColorPrinter:
    WHITE = '\033[1;47;30m'
    BLACK = '\033[1;40;37m'

    ENDC  = '\033[0m'

    def bla(clas):
        print "bla"

    @staticmethod
    def output(b, (i, j)):
        white = ((i+j)%2 == 1)
        cell = b[i][j]
        if cell is None:
            sign = ' '
        else:
            sign = cell['p']
        if white:
            return AnsiColorPrinter.WHITE + ' ' + sign + ' ' + AnsiColorPrinter.ENDC
        else:
            return AnsiColorPrinter.BLACK + ' ' + sign + ' ' + AnsiColorPrinter.ENDC
    # WHITE = '\033[97;100m'
    # BLACK = '\033[90;107m'

class Board:
    utf8 = False
    ansiColors = True
    printer = AnsiColorPrinter

    b = [[None for x in xrange(8)] for y in xrange(8)]
    
    def __init__(self):
        if self.ansiColors:
            self.printer = AnsiColorPrinter
        else:
            self.printer = WithoutColorPrinter

    def __getitem__(self, key):
        pass

    def __setitem__(self, key, value):
        pass

    def __str__(self):
        rStr = "\n     a  b  c  d  e  f  g  h     \n"
        for j in range(8)[::-1]:
            rStr += "  "  + str(j+1) + " "
            for i in range(8):
                rStr += self.printer.output(self.b, (j, i))
            rStr += " "  + str(j+1)
            rStr += "\n"
        rStr += "     a  b  c  d  e  f  g  h     \n"
        return rStr



class C:
    W = 0
    B = 1

class P:
    T = 'T'
    B = 'B'

b = Board()
b.b[3][4] = {'p': P.T, 'c': C.W}
b.b[4][4] = {'p': P.B, 'c': C.B}

print b