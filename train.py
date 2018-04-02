import os
import time

import numpy as np
import tqdm

import game
from states import *


def change_prob(p, i, v):
    if max(0, p[i]+v) == 0:
        return p
    p[i] += v
    s     = sum(p)
    return [j/s for j in p]


if os.path.exists('states.npy'):
    states = load_states()
else:
    states = np.unique(generate_states(), axis=0)
    save_states(states)
states = states.tolist()


q_mat = np.array([[0]*9]*len(states), dtype=np.float32)
for i, state in enumerate(tqdm.tqdm(states, "Generating Q matrix")):
    moves = game.Board(state).valid_moves()
    prob  = 1/len(moves)
    for move in moves:
        q_mat[i][move] = prob


board = game.Board()
for i in tqdm.trange(100000, desc="Training"):
    board.reset()

    #x_moves = np.array([], dtype=np.int32)
    #o_moves = np.array([], dtype=np.int32)
    x_moves = []
    o_moves = []

    state = 0
    while not state:
        index = states.index(board.board.tolist())
        moves = q_mat[index]
        move  = np.random.choice(9, p=moves)
        if board.player == 0:
            #x_moves = np.append(x_moves, [move, index])
            x_moves.append([move, index])
        if board.player == 1:
            #o_moves = np.append(o_moves, [move, index])
            o_moves.append([move, index])
        state = board.play(move)

    #x_moves.shape = (-1, 2)
    #o_moves.shape = (-1, 2)

    for i, x_move in enumerate(x_moves):
        if state == 1:
            q_mat[x_move[1]] = change_prob(q_mat[x_move[1]], x_move[0], i+1)
        if state == 2:
            pass
            #q_mat[x_move[1]] = change_prob(q_mat[x_move[1]], x_move[0], -i)
        if state == 3:
            q_mat[x_move[1]] = change_prob(q_mat[x_move[1]], x_move[0], (i+1)/2)

    for i, o_move in enumerate(o_moves):
        if state == 1:
            pass
            #q_mat[o_move[1]] = change_prob(q_mat[o_move[1]], o_move[0], -i)
        if state == 2:
            q_mat[o_move[1]] = change_prob(q_mat[o_move[1]], o_move[0], i+1)
        if state == 3:
            q_mat[o_move[1]] = change_prob(q_mat[o_move[1]], o_move[0], (i+1)/2)

while True:
    board.reset()
    state = 0
    while not state:
        os.system('clear')
        index     = states.index(board.board.tolist())
        move_prob = q_mat[index]
        print(move_prob)
        move      = np.random.choice(9, p=move_prob)
        state     = board.play(move)
        if state:
            break
        board.print()

        state = board.play(int(input()))

