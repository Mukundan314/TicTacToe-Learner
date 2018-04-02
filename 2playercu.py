import game

from curses import wrapper
import curses
import os


def main(stdscr):
    stdscr.clear()
    curses.use_default_colors()
    x = 0
    y = 0

    board = game.Board()
    state = 0
    while not state:
        board.curses_print(stdscr, y, x)
        move = {
            55: 0, 56: 1, 57: 2,
            52: 3, 53: 4, 54: 5,
            49: 6, 50: 7, 51: 8
        }[stdscr.getch()]
        state = board.play(move)
        stdscr.refresh()

    if state == 1:
        stdscr.addstr(y+8, x, "X won")
    if state == 2:
        stdscr.addstr(y+8, x, "O won")
    if state == 3:
        stdscr.addstr(y+8, x, "Draw")

    stdscr.getch()


if __name__ == "__main__":
    wrapper(main)
