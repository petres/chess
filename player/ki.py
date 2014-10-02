# -*- coding: utf-8 -*-

import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from player import Player
import random
from base import *

class Random(Player):
    def move(self, board):
        pos = board.getPossibleMoves(self.color)
        piece = random.choice(list(pos.keys()))
        field = random.choice(pos[piece])
        return (piece, field)


class KillBill(Player):
    def move(self, board):
        pos = board.getPossibleMoves(self.color)
        for piece in pos:
            for field in pos[piece]:
                if board[field] != None:
                    return (piece, field)

        piece = random.choice(list(pos.keys()))
        field = random.choice(pos[piece])
        return (piece, field)


class KillBest(Player):
    p = {
        Queen:   9,
        Rook:    7,
        Knight:  4,
        Bishop:  4,
        Pawn:    1
    }
    def move(self, board):
        pos = board.getPossibleMoves(self.color)
        posCaptures = []
        posBetterMoves = []
        for piece in pos:
            for field in pos[piece]:
                if board[field] != None:
                    posCaptures.append((piece, field))

                if not board.isFieldThreaten(field, self.color.O):
                    posBetterMoves.append((piece, field))

        best = 0
        bestMove = None
        for pc in posCaptures:
            o, t = pc
            print("should i capture field", board.tN(t), "with", board.tN(o))
            print("there is a", board[t].__class__)
            b = self.p[board[t].__class__]
            if board.isFieldThreaten(t, self.color.O):
                print
                b -= self.p[board[o].__class__]
            else:
                print("and the field isnt dirty")

            if b > best:
                print("t:", board[t].__class__.__name__, "o:", board[o].__class__.__name__, "b:", b)
                bestMove = pc

        if bestMove:
            print("capturing yeah")
            return bestMove


        if len(posBetterMoves) > 0:
            print("moving to some not dirty place")
            return random.choice(posBetterMoves)

        piece = random.choice(list(pos.keys()))
        field = random.choice(pos[piece])
        return (piece, field)
        