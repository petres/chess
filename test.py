#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base import *


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

print(BishopMovements('C4'))

print(PawnMovements('C2', C.W))
print(PawnMovements('C2', C.B))

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