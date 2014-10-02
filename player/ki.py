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
        