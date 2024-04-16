import curses as cs

def load_puzzle(path: str) -> tuple[list[list[str]], tuple[int, int]]:
    start = (0, 0)
    board = []
    with open(path, "r") as file:
        for row, line in enumerate(file):
            board.append(list(line.strip()))
            start_col = line.find("S")

            if line.find("S") > 0:
                start = (row, start_col)

    return board, start


def possible_moves(board, cursr):
    moves = []

    if board[cursr[0]+1][cursr[1]] not in ("█", "*", "S"):
        moves.append((1, 0))

    if board[cursr[0]-1][cursr[1]] not in ("█", "*", "S"):
        moves.append((-1, 0))

    if board[cursr[0]][cursr[1]+1] not in ("█", "*", "S"):
        moves.append((0, 1))

    if board[cursr[0]][cursr[1]-1] not in ("█", "*", "S"):
        moves.append((0, -1))

    return moves


def update_and_draw(win: cs.window, board, pos, char, ms):
    if board[pos[0]][pos[1]] != "S":
        board[pos[0]][pos[1]] = char

        win.move(pos[0], pos[1])
        win.addch(char)
        win.refresh()
        cs.napms(ms)


def traverse(win: cs.window, board, cpos):
    found = board[cpos[0]][cpos[1]] == "G"
    while not found:
        moves = possible_moves(board, cpos)
        if len(moves) == 1:
            update_and_draw(win, board, cpos, "*", 50)

            cpos = (cpos[0] + moves[0][0], cpos[1] + moves[0][1])

            if board[cpos[0]][cpos[1]] == "G":
                return board, True
        elif len(moves) > 1:
            for move in moves:
                update_and_draw(win, board, cpos, "*", 50)

                board, found = traverse(win, board, (cpos[0] + move[0], cpos[1] + move[1]))

                if found:
                    break
        else:
            update_and_draw(win, board, cpos, "*", 50)

            return board, False

    return board, found


def main(stdscr: cs.window):
    cs.start_color()
    cs.use_default_colors()
    cs.curs_set(0)

    cs.init_pair(1, cs.COLOR_RED, -1)
    cs.init_pair(2, cs.COLOR_GREEN, -1)

    board, start = load_puzzle("puzzle1.txt")

    stdscr.clear()

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

    traverse(stdscr, board, start)

    stdscr.getkey()


if __name__ == "__main__":
    cs.wrapper(main)
