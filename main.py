import curses as cs
from util import Coord, Board

def possible_moves(board: Board, pos: Coord):
    moves = []

    if board[pos + Coord(1, 0)] not in ("█", "*", "S"):
        moves.append(Coord(1, 0))

    if board[pos + Coord(-1, 0)] not in ("█", "*", "S"):
        moves.append(Coord(-1, 0))

    if board[pos + Coord(0, 1)] not in ("█", "*", "S"):
        moves.append(Coord(0, 1))

    if board[pos + Coord(0, -1)] not in ("█", "*", "S"):
        moves.append(Coord(0, -1))

    return moves


def update_and_draw(win: cs.window, board: Board, pos: Coord, char, ms):
    if board[pos] != "S":
        board[pos] = char

        win.move(pos.y, pos.x)
        win.addch(char)
        win.refresh()
        cs.napms(ms)


def traverse(win: cs.window, board: Board, pos: Coord):
    found = board[pos] == "G"
    while not found:
        if board[pos] != "*":
            update_and_draw(win, board, pos, "*", 50)

        moves = possible_moves(board, pos)

        if len(moves) == 1:
            pos = pos + moves[0]

            if board[pos] == "G":
                return board, True

        elif len(moves) > 1:
            for move in moves:
                board, found = traverse(win, board, pos + move)

                if found:
                    break
        else:
            return board, False

    return board, found


def main(stdscr: cs.window):
    cs.start_color()
    cs.use_default_colors()
    cs.curs_set(0)

    cs.init_pair(1, cs.COLOR_RED, -1)
    cs.init_pair(2, cs.COLOR_GREEN, -1)

    board = Board("puzzle1.txt")

    for i, row in enumerate(board):
        stdscr.addstr(f'{"".join(row)}\n')

        if "S" in row:
            stdscr.move(i, row.index("S"))
            stdscr.addch("█", cs.color_pair(2))
            stdscr.move(i+1, 0)
            stdscr.refresh()
        elif "G" in row:
            stdscr.move(i, row.index("G"))
            stdscr.addch("█", cs.color_pair(1))
            stdscr.move(i+1, 0)
            stdscr.refresh()

    traverse(stdscr, board, board.start)

    stdscr.getkey()


if __name__ == "__main__":
    cs.wrapper(main)
