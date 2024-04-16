import curses as cs

class Coord:
    def __init__(self, y=0, x=0):
        self.set(y, x)


    def __add__(self, other):
        self.y = self.y + other.y
        self.x = self.x + other.x

        return self.copy()

    def __str__(self):
        return f"{(self.x, self.y)}"

    def set(self, y=None, x=None):
        self.y = y or 0
        self.x = x or 0


    def copy(self):
        return Coord(self.y, self.x)


def load_puzzle(path: str) -> tuple[list[list[str]], Coord]:
    start = Coord()
    board = []
    with open(path, "r") as file:
        for row, line in enumerate(file):
            board.append(list(line.strip()))
            start_col = line.find("S")

            if line.find("S") > 0:
                start.set(row, start_col)

    return board, start


def possible_moves(board, pos: Coord) -> list[Coord]:
    moves = []

    if board[pos.y+1][pos.x] not in ("█", "*", "S"):
        moves.append(Coord(1, 0))

    if board[pos.y-1][pos.x] not in ("█", "*", "S"):
        moves.append(Coord(-1, 0))

    if board[pos.y][pos.x+1] not in ("█", "*", "S"):
        moves.append(Coord(0, 1))

    if board[pos.y][pos.x-1] not in ("█", "*", "S"):
        moves.append(Coord(0, -1))

    return moves


def update_and_draw(win: cs.window, board, pos: Coord, char, ms):
    if board[pos.y][pos.x] != "S":
        board[pos.y][pos.x] = char

        win.move(pos.y, pos.x)
        win.addch(char)
        win.refresh()
        cs.napms(ms)

    return board


def traverse(win: cs.window, board, pos: Coord):
    found = board[pos.y][pos.x] == "G"
    while not found:
        moves = possible_moves(board, pos)
        if len(moves) == 1:
            board = update_and_draw(win, board, pos, "*", 10)

            pos = pos + moves[0]

            if board[pos.y][pos.x] == "G":
                return board, True
        elif len(moves) > 1:
            for move in moves:
                board = update_and_draw(win, board, pos, "*", 10)

                board, found = traverse(win, board, pos + move)

                if found:
                    break
        else:
            board = update_and_draw(win, board, pos, "*", 10)

            return board, False

    return board, found


def main(stdscr: cs.window):
    cs.start_color()
    cs.use_default_colors()
    cs.curs_set(0)

    cs.init_pair(1, cs.COLOR_RED, -1)
    cs.init_pair(2, cs.COLOR_GREEN, -1)

    board, start = load_puzzle("puzzle1.txt")

    stdscr.move(0, 0)
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
