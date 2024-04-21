from util import Board
import curses as cs
import string
import time
import algo


def main(stdscr: cs.window):
    cs.start_color()
    cs.use_default_colors()
    cs.curs_set(0)

    cs.init_pair(1, cs.COLOR_RED, cs.COLOR_BLACK)
    cs.init_pair(2, cs.COLOR_GREEN, cs.COLOR_BLACK)
    cs.init_pair(3, cs.COLOR_BLACK, 215)
    cs.init_pair(4, cs.COLOR_WHITE, cs.COLOR_BLACK)
    cs.init_pair(5, 237, cs.COLOR_BLACK)
    cs.init_pair(6, cs.COLOR_WHITE, cs.COLOR_WHITE)

    board = Board("puzzle7.txt")

    for i, row in enumerate(board):
        for e in row:
            if e in string.digits:
                stdscr.addch(e, cs.color_pair(5))
            elif e == "█":
                stdscr.addch(" ", cs.color_pair(6))
            else:
                stdscr.addch(e, cs.color_pair(4))

        if "S" in row:
            stdscr.move(i, row.index("S"))
            stdscr.addch("█", cs.color_pair(2))
        if "G" in row:
            stdscr.move(i, row.index("G"))
            stdscr.addch("█", cs.color_pair(1))

        stdscr.move(i+1, 0)


    stdscr.move(board.height + 2, 0)
    stdscr.addstr("Press any key to continue...")
    stdscr.getkey()
    stdscr.move(board.height + 2, 0)
    stdscr.addstr("                            ")

    start = time.time()
    goal, paths, states = algo.a_star(stdscr, board)
    end = time.time()

    for path in paths:
        stdscr.move(path.y, path.x)
        stdscr.addch("•", cs.color_pair(3))

    stdscr.refresh()

    stdscr.move(board.height+3, 0)
    stdscr.addstr(f"Goal found at   : {goal}\n")
    stdscr.addstr(f"Number of states: {states}\n")
    stdscr.addstr(f"Time taken      : {end - start:.2f} s\n")

    stdscr.getkey()


if __name__ == "__main__":
    cs.wrapper(main)
