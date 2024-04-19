from collections.abc import Callable
import curses as cs

from util import Coord, Board, PQueue

def possible_moves(board: Board, pos: Coord):
    moves = []

    if board[pos + Coord(0, 1)] not in ("█", ".", "S"):
        moves.append(Coord(0, 1))

    if board[pos + Coord(1, 0)] not in ("█", ".", "S"):
        moves.append(Coord(1, 0))

    if board[pos + Coord(0, -1)] not in ("█", ".", "S"):
        moves.append(Coord(0, -1))

    if board[pos + Coord(-1, 0)] not in ("█", ".", "S"):
        moves.append(Coord(-1, 0))

    return moves


def update_and_draw(win: cs.window, board: Board, pos: Coord, char, ms):
    if board[pos] != "S" and board[pos] != "G":
        board[pos] = char

        win.move(pos.y, pos.x)
        win.addch(char)
        win.refresh()
        cs.napms(ms)


def dfs(win: cs.window, board: Board, start: Coord):
    stack = []

    board[start] = "."
    stack.append((start, [start]))

    while len(stack) > 0:
        vpos, path = stack.pop()

        update_and_draw(win, board, vpos, ".", 0)

        path = path.copy()

        if board[vpos] == "G":
            return vpos, path

        moves = possible_moves(board, vpos)
        for move in moves:
            adjacent = vpos + move
            if board[adjacent] != "*":
                update_and_draw(win, board, adjacent, "*", 20)
                stack.append((adjacent, path + [vpos]))

    return start, []


def bfs(win: cs.window, board: Board, start: Coord):
    queue = []

    board[start] = "."
    queue.append((start, [start]))

    while len(queue) > 0:
        vpos, path = queue.pop(0)

        update_and_draw(win, board, vpos, ".", 0)

        path = path.copy()

        if board[vpos] == "G":
            return vpos, path

        moves = possible_moves(board, vpos)

        for move in moves:
            adjacent = vpos + move
            if board[adjacent] != "*":
                update_and_draw(win, board, adjacent, "*", 20)
                queue.append((adjacent, path + [vpos]))

    return start, []


def ucs(win: cs.window, board: Board, start: Coord, goal: Coord):
    frontier = PQueue()
    expanded = []

    frontier.insert(start, 0)

    while not frontier.empty():
        vpos, _ = frontier.min()

        update_and_draw(win, board, vpos, ".", 0)

        if board[vpos] == "G":
            return vpos, expanded

        expanded.append(vpos)

        moves = possible_moves(board, vpos)
        for move in moves:
            adjacent = vpos + move
            cost = Coord.dist(adjacent, goal)
            if adjacent not in expanded and adjacent not in frontier:
                update_and_draw(win, board, adjacent, "*", 20)
                frontier.insert(adjacent, cost)
            elif adjacent in frontier:
                if cost < frontier.get(adjacent):
                    frontier.update(adjacent, cost)


    return start, []


def main(stdscr: cs.window):
    cs.start_color()
    cs.use_default_colors()
    cs.curs_set(0)

    cs.init_pair(1, cs.COLOR_RED, -1)
    cs.init_pair(2, cs.COLOR_GREEN, -1)
    cs.init_pair(3, cs.COLOR_BLACK, cs.COLOR_YELLOW)

    board = Board("puzzle2.txt")

    for i, row in enumerate(board):
        stdscr.addstr(f'{"".join(row)}\n')

        if "S" in row:
            stdscr.move(i, row.index("S"))
            stdscr.addch("█", cs.color_pair(2))
            stdscr.move(i+1, 0)
            stdscr.refresh()
        if "G" in row:
            stdscr.move(i, row.index("G"))
            stdscr.addch("█", cs.color_pair(1))
            stdscr.move(i+1, 0)
            stdscr.refresh()

    goal, paths = ucs(stdscr, board, board.start, board.goal)

    for path in paths[1:]:
        stdscr.move(path.y, path.x)
        stdscr.addch(".", cs.color_pair(3))

    stdscr.refresh()

    stdscr.move(board.height + 1, 0)
    stdscr.addstr(f"Goal found at: {goal}")

    stdscr.getkey()


if __name__ == "__main__":
    cs.wrapper(main)
