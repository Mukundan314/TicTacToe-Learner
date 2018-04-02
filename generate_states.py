import os
import numpy as np
import game


def generate_states(board=game.Board([[0, 0, 0],
                                      [0, 0, 0],
                                      [0, 0, 0]])):
    states = [board.board]
    for move in board.valid_moves():
        tmp = board.copy()
        if (tmp.play(move)):
            continue
        states.extend(generate_states(tmp))
    return states


def load_states(filename='states.npy'):
    states = np.load(filename).tolist()
    return states


def save_states(states, filename='states.npy'):
    np.save(filename, np.array(states))


if __name__ == '__main__':
    if not  os.path.exists('states.npy'):
        states = np.unique(generate_states(), axis=0).tolist()
        save_states(states)
