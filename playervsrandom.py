import os
import random

import game

player = {
    'y': 0,
    'Y': 0,
    'yes': 0,
    'Yes': 0,
    'n': 1,
    'N': 1,
    'no': 1,
    'No': 1
}[input('Do you want to go first: ')]

board = game.Board()
state = 0
while not state:
    if board.player == player:
        os.system('clear')
        board.print()
        state = board.play(int(input('Your Move: ')))
        if state == -1:
            state = 0
    else:
        moves = board.valid_moves()
        move = random.choice(moves)
        state = board.play(move)

board.print()
