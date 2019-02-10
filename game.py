import curses

import numpy as np

__all__ = ['Board']


class Board():
    def __init__(self, board=np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])):
        self.board = board
        self.player = np.count_nonzero(board) % 2

    def reset(self):
        self.board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.player = 0

    def winner(self):
        if np.count_nonzero(self.board) == 9:
            return 3

        if self.board[0, 0] == self.board[1, 1] == self.board[2, 2]:
            return self.board[0, 0]
        if self.board[0, 2] == self.board[1, 1] == self.board[2, 0]:
            return self.board[0, 2]

        if self.board[0, 0] == self.board[1, 0] == self.board[2, 0]:
            return self.board[0, 0]
        if self.board[0, 1] == self.board[1, 1] == self.board[2, 1]:
            return self.board[0, 1]
        if self.board[0, 2] == self.board[1, 2] == self.board[2, 2]:
            return self.board[0, 2]

        if self.board[0, 0] == self.board[0, 1] == self.board[0, 2]:
            return self.board[0, 0]
        if self.board[1, 0] == self.board[1, 1] == self.board[1, 2]:
            return self.board[1, 0]
        if self.board[2, 0] == self.board[2, 1] == self.board[2, 2]:
            return self.board[2, 0]

    def play(self, position):
        if not self.board[position // 3, position % 3]:
            self.board[position // 3, position % 3] = self.player + 1
            self.player += 1
            self.player %= 2
            return self.winner()
        else:
            return -1

    def valid_moves(self):
        moves = []
        for i in range(9):
            if not self.board[i // 3][i % 3]:
                moves.append(i)
        return moves

    def print(self):
        print('\033[1m')
        print('┏━━━┳━━━┳━━━┓')

        for row in range(3):
            for column in range(3):
                player = {0: ' ', 1: 'X', 2: 'O'}[self.board[row][column]]
                print('┃ ' + player, end=' ')

            print('┃')
            if row != 2:
                print('┣━━━╋━━━╋━━━┫')

        print('┗━━━┻━━━┻━━━┛')
        print('\033[0m')

    def curses_print(self, stdscr, y, x):
        stdscr.addstr(y, x, '┏━━━┳━━━┳━━━┓')

        for row in range(3):
            y1 = y + 2 * row + 1
            for column in range(3):
                x1 = x + column * 4

                player = {0: ' ', 1: 'X', 2: 'O'}[self.board[row][column]]
                stdscr.addstr(y1, x1, '┃ ' + player, curses.A_BOLD)

            stdscr.addch(y1, x + 12, '┃')
            if row != 2:
                stdscr.addstr(y1 + 1, x, '┣━━━╋━━━╋━━━┫')

        stdscr.addstr(y + 6, x, '┗━━━┻━━━┻━━━┛')

    def copy(self):
        tmp_board = Board()
        tmp_board.board = np.copy(self.board)
        tmp_board.player = self.player
        return tmp_board
