# -*- coding: utf-8 -*-

import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from player import Player

from base import *

class Terminal(Player):
    def move(self, board):
        while True: 
            kIn = input("\n Your move: ")
            if len(kIn) == 4:
                return (kIn[:2],kIn[2:])

        
