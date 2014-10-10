# -*- coding: utf-8 -*-
import os, sys, random
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from player import Player
from base import *

kiClasses = {}

def promoteKI(oClass):
    #print(oClass.__name__)
    kiClasses[oClass.__name__] = oClass
    return oClass

def getKiClasses():
    return kiClasses

class KiPlayer(Player):
    pieceValues = {}
    def getValueOfPiece(self, piece):
        return self.pieceValues[piece.__class__.__name__]

@promoteKI
class PureRandom(Player):
    def move(self, board):
        possibleMoves = board.getPossibleMoves(self.color)
        piece = random.choice(list(possibleMoves.keys()))
        field = random.choice(possibleMoves[piece])
        return (piece.pos, field)

@promoteKI
class KillBill(Player):
    def move(self, board):
        possibleMoves = board.getPossibleMoves(self.color)
        for piece in possibleMoves:
            for field in possibleMoves[piece]:
                if board[field] != None:
                    return (piece.pos, field)

        piece = random.choice(list(pos.keys()))
        return (piece.pos, random.choice(pos[piece]))

@promoteKI
class KillBest(KiPlayer):
    pieceValues = { "Queen":   9,
                    "Rook":    7,
                    "Knight":  4,
                    "Bishop":  4,
                    "Pawn":    1 }

    def move(self, board):
        possibleMoves = board.getPossibleMoves(self.color)
        posCaptures = []
        posBetterMoves = []
        posCheck = []
        for piece in possibleMoves:
            #fieldInfo = board.fieldInfo(piece.pos)
            for field in possibleMoves[piece]:
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
            b = self.getValueOfPiece(board[t])
            if board.isFieldThreaten(t, self.color.O):
                b -= self.getValueOfPiece(board[o])

            if b > best:
                bestMove = pc

        if bestMove:
            return bestMove

        if len(posCheck) > 0:
            return random.choice(posCheck)

        if len(posBetterMoves) > 0:
            return random.choice(posBetterMoves)

        piece = random.choice(list(possibleMoves.keys()))
        return (piece.pos, random.choice(possibleMoves[piece]))

