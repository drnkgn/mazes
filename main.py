from utils.board import Board
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

    board = Board("puzzle1.txt")

    board_win = cs.newwin(board.height+1, cs.COLS, 0, 0)
    debug_win = cs.newwin(10, cs.COLS, board.height+2, 0)

    for i, row in enumerate(board):
        for e in row:
            if e in string.digits:
                board_win.addch(e, cs.color_pair(5))
            elif e == "█":
                board_win.addch(" ", cs.color_pair(6))
            else:
                board_win.addch(e, cs.color_pair(4))

        if "S" in row:
            board_win.move(i, row.index("S"))
            board_win.addch("█", cs.color_pair(2))
        if "G" in row:
            board_win.move(i, row.index("G"))
            board_win.addch("█", cs.color_pair(1))

        board_win.move(i+1, 0)


    board_win.refresh()

    debug_win.addstr("Press any key to continue...")
    debug_win.getkey()
    debug_win.move(0, 0)
    debug_win.addstr("                            ")
    debug_win.refresh()

    start = time.time()
    goal, paths, states = algo.ucs(board_win, board)
    end = time.time()

    for path in paths:
        board_win.move(path.y, path.x)
        board_win.addch("•", cs.color_pair(3))

    board_win.refresh()

    debug_win.move(1, 0)
    debug_win.addstr(f"Goal found at   : {goal}\n")
    debug_win.addstr(f"Number of states: {states}\n")
    debug_win.addstr(f"Time taken      : {end - start:.2f} s\n")
    debug_win.refresh()

    debug_win.getkey()


if __name__ == "__main__":
    cs.wrapper(main)
