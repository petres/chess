#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, sys, time, signal

sys.path.append(os.path.join(os.path.dirname(__file__), "player"))

from base import *
from settings import *

from human import *
from ki import *



def run():
	def handler(signum = None, frame = None):
		print(b)
		sys.exit(0)

	b = Board()

	b.setStartPosition();

	pW = KillBest(C.W)
	pB = KillBill(C.B)

	print(b)

	for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
		signal.signal(sig, handler)

	while True:
		for p in [pW, pB]:
			status = b.getStatus(p.color);
			if status != GameStatus.NotFinished:
				if status == GameStatus.StaleMate:
					print("Stale Mate for " + p.color.name)
				else:
					print("Check Mate for " + p.color.name)
				print(b)
				exit();

			while True:
				piecePos, toPos = p.move(b)
				if b.move(piecePos, toPos):
					break
			b.writeFile("last")
			#print(b)

if __name__ == "__main__":
	run()

	


		
			
