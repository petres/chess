#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base import *


class Player:
    def pleaseMove(self, board):
        # calculate possibiliees
        # calculate for every pos. the value
        # return best move
        pass

# r = RookMovements('C4')
# print(r)

# r = KingMovements('H7')
# print(r)

# r = KnightMovements('H7')
# print(r)

# print(BishopMovements('C4'))

#print(PawnMovements('C2', C.W))
#print(PawnMovements('C2', C.B))

b = Board()

b.setStartPosition();
# b.move("a2", "a4")
# b.move("b7", "b5")
# b.move("b2", "b4")
# b.move("a4", "b5")
# b.move("c2", "c4")
# b.move("c1", "b2")
# b.move("b1", "a3")

# b['E7'] = King(C.B)
# b['A3'] = Pawn(C.B)
# b['A1'] = Bishop(C.B)

# print(b['E7'])
# print(b['A3'])

# print(b['E7'].moveIns)
# print(b['A3'].moveIns)

# exit()

#b['D7'] = King(C.W)
# b['E8'] = {'p': Queen, 'c': C.B}
# b['C4'] = {'p': Rock, 'c': C.W}
# b['D4'] = {'p': Bishop, 'c': C.W}

# b[(1, 3)] = {'p': P.P, 'c': C.W}

#print(b['A1'])

#print(b)



while True:
	print(b)
	kIn = input("\nInput: ")
	if " " in kIn or len(kIn) == 1:
		cmd = kIn.split(" ")
		fileName = Settings.fileName 
		if len(cmd) == 2:
			fileName = cmd[1]

		if cmd[0] == "e":
			print("Exporting")
			b.writeFile(fileName)
		elif cmd[0] == "i":
			print("Importing")
			b = Board.readFile(fileName)
	if len(kIn) == 0:
		break
	if len(kIn) == 2:
		if kIn == "pw":
			b.printPossibleMoves(b.getPossibleMoves(C.W))
		elif kIn == "pb":
			b.printPossibleMoves(b.getPossibleMoves(C.B))
		else:
			print(b[kIn])
	if len(kIn) == 4:
		b.move(kIn[:2],kIn[2:])


		
			
