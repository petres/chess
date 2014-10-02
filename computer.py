#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "player"))

from base import *
from settings import *

from human import *
from ki import *

import time



b = Board()

b.setStartPosition();

pW = Terminal(C.W)
pB = KillBill(C.B)

print(b)

while True:
	for p in [pW, pB]:
		while True:
			piecePos, toPos = p.move(b)
			if b.move(piecePos, toPos):
				break

		print(b)
		time.sleep(0.5)

	


		
			
