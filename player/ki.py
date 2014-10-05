# -*- coding: utf-8 -*-

import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from player import Player
import random
from base import *

class PureRandom(Player):
    def move(self, board):
        pos = board.getPossibleMoves(self.color)
        piece = random.choice(list(pos.keys()))
        field = random.choice(pos[piece])
        return (piece.pos, field)


class KillBill(Player):
    def move(self, board):
        pos = board.getPossibleMoves(self.color)
        for piece in pos:
            for field in pos[piece]:
                if board[field] != None:
                    return (piece.pos, field)

        piece = random.choice(list(pos.keys()))
        field = random.choice(pos[piece])
        return (piece.pos, field)


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
        posCheck = []
        for piece in pos:
            #fieldInfo = board.fieldInfo(piece.pos)
            for field in pos[piece]:
                if board[field] != None:
                    posCaptures.append((piece.pos, field))

                if not board.isFieldThreaten(field, self.color.O):
                    posBetterMoves.append((piece.pos, field))

                if board.isCheckAfterMove(piece, field, self.color.O) and not board.isFieldThreaten(field, self.color.O):
                    posCheck.append((piece.pos, field))

        best = 0
        bestMove = None
        for pc in posCaptures:
            o, t = pc
            b = self.p[board[t].__class__]
            if board.isFieldThreaten(t, self.color.O):
                b -= self.p[board[o].__class__]

            if b > best:
                bestMove = pc

        if bestMove:
            return bestMove

        if len(posCheck) > 0:
            return random.choice(posCheck)

        if len(posBetterMoves) > 0:
            return random.choice(posBetterMoves)



        piece = random.choice(list(pos.keys()))
        field = random.choice(pos[piece])
        return (piece.pos, field)
        