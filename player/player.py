# -*- coding: utf-8 -*-
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from settings import *

class Player:
    color = None

    def __init__(self, color = None):
        self.color = color

    def move(self, board):
        pass
