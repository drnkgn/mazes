from util import Board
import curses as cs
import algo

def main(stdscr: cs.window):
    cs.start_color()
    cs.use_default_colors()
    cs.curs_set(0)

    cs.init_pair(1, cs.COLOR_RED, -1)
    cs.init_pair(2, cs.COLOR_GREEN, -1)
    cs.init_pair(3, cs.COLOR_BLACK, cs.COLOR_YELLOW)
    cs.init_pair(4, cs.COLOR_WHITE, cs.COLOR_BLACK)

    board = Board("puzzle6.txt")

    for i, row in enumerate(board):
        stdscr.addstr(f'{"".join(row)}\n', cs.color_pair(4))

        if "S" in row:
            stdscr.move(i, row.index("S"))
            stdscr.addch("█", cs.color_pair(2))
            stdscr.move(i+1, 0)
        if "G" in row:
            stdscr.move(i, row.index("G"))
            stdscr.addch("█", cs.color_pair(1))
            stdscr.move(i+1, 0)

    goal, paths = algo.bfs(stdscr, board)

    for path in paths:
        stdscr.move(path.y, path.x)
        stdscr.addch(".", cs.color_pair(3))

    stdscr.refresh()

    stdscr.move(board.height + 1, 0)
    stdscr.addstr(f"Goal found at: {goal}")

    stdscr.getkey()


if __name__ == "__main__":
    cs.wrapper(main)
