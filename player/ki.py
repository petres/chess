# -*- coding: utf-8 -*-
import os, sys, random
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from player import Player
from base import *

kiClasses = {}

class KiPlayer(Player):
    promotedKIPlayers = {}
    pieceValues = {}
    
    def getValueOfPiece(self, piece):
        return self.pieceValues[piece.__class__.__name__]
    
    @staticmethod
    def getPromotedKiPlayers():
        return KiPlayer.promotedKIPlayers


def promoteKI(oClass):
    KiPlayer.promotedKIPlayers[oClass.__name__] = oClass
    return oClass


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

        piece = random.choice(list(possibleMoves.keys()))
        return (piece.pos, random.choice(possibleMoves[piece]))


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



# @promoteKI
# class KillAndAtLeastTryToDefend(KiPlayer):
#     pieceValues = { "Queen":   9,
#                     "Rook":    7,
#                     "Knight":  4,
#                     "Bishop":  4,
#                     "Pawn":    1 }
#     def move(self, board):
#         possibleMoves = board.getPossibleMoves(self.color)
#         posCaptures = []
#         posBetterMoves = []
#         posCheck = []
#         for piece in possibleMoves:
#             fieldInfo = board.fieldInfo(piece.pos)
#             # piece is threaten
#             if fieldInfo["t"][self.color.O] > 0:
#                 possibleLost = self.getValueOfPiece(piece)
#                 if fieldInfo["t"][self.color] > 0:
                    


#             for field in possibleMoves[piece]:
#                 if board[field] != None:
#                     posCaptures.append((piece.pos, field))

#                 if not board.isFieldThreaten(field, self.color.O):
#                     posBetterMoves.append((piece.pos, field))

#                 if board.isCheckAfterMove(piece, field, self.color.O) and not board.isFieldThreaten(field, self.color.O):
#                     posCheck.append((piece.pos, field))

#         best = 0
#         bestMove = None
#         for pc in posCaptures:
#             o, t = pc
#             b = self.getValueOfPiece(board[t])
#             if board.isFieldThreaten(t, self.color.O):
#                 b -= self.getValueOfPiece(board[o])

#             if b > best:
#                 bestMove = pc

#         if bestMove:
#             return bestMove

#         if len(posCheck) > 0:
#             return random.choice(posCheck)

#         if len(posBetterMoves) > 0:
#             return random.choice(posBetterMoves)

#         piece = random.choice(list(possibleMoves.keys()))
#         return (piece.pos, random.choice(possibleMoves[piece]))


@promoteKI
class FirstStep(KiPlayer):
    pieceValues = { "Queen":   9,
                    "Rook":    7,
                    "Knight":  4,
                    "Bishop":  4,
                    "Pawn":    1 }

    def move(self, board):
        possibleMoves   = board.getPossibleMoves(self.color)
        posCaptures     = []
        posBetterMoves  = []
        posCheck        = []

        coded = board.getCodedPosition()
        for piece in possibleMoves:
            for field in possibleMoves[piece]:
                print()
                print("before move", board.tN(piece.pos), "->", board.tN(field), "piece id", id(piece), "field piece id", id(board[piece.pos]))
                board.move(piece.pos, field)
                print("after move", board.tN(piece.pos), id(board[field]))
                # coded2 = board.getCodedPosition()
                # possibleMovesO = board.getPossibleMoves(self.color.O)
                # for pieceO in possibleMovesO:
                #     for fieldO in possibleMovesO[pieceO]:
                #         print("s", board.tN(pieceO.pos), "->", board.tN(fieldO))
                #         board.move(pieceO.pos, fieldO)
                #         board.loadCodedPosition(coded2)
                #         print("s", board.tN(pieceO.pos), "->", board.tN(fieldO))
                board.loadCodedPosition(coded)
                print("after load", board.tN(piece.pos))
        
        board.loadCodedPosition(coded)
        
        possibleMoves = board.getPossibleMoves(self.color)
        piece = random.choice(list(possibleMoves.keys()))
        field = random.choice(possibleMoves[piece])
        return (piece.pos, field)
