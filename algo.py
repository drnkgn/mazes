import curses as cs
from util import Coord, Board, PQueue

def possible_moves(board: Board, pos: Coord) -> list[Coord]:
    """
    Returns a list of possible from the current position.
    """
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


def update_and_draw(win: cs.window,
                    board: Board,
                    pos: Coord,
                    char: str,
                    ms: int) -> None:
    """
    Updates position on the board as visited both internally and during the
    animation.
    """
    if board[pos] != "S" and board[pos] != "G":
        board[pos] = char

        win.move(pos.y, pos.x)
        win.addch(char)
        win.refresh()
        cs.napms(ms)


"""
Below are the searching algorithm implementations. All of them returns
the goal position and the path that it founds.
"""

def dfs(win: cs.window, board: Board):
    stack = [board.start]
    paths = [[board.start]]

    while len(stack) > 0:
        vpos = stack.pop()
        path = paths.pop().copy()

        update_and_draw(win, board, vpos, ".", 0)

        if board[vpos] == "G":
            return vpos, path[2:]

        moves = possible_moves(board, vpos)
        for move in moves:
            adjacent = vpos + move
            if board[adjacent] != "*":
                update_and_draw(win, board, adjacent, "*", 20)
                stack.append(adjacent)
                paths.append(path + [vpos])

    return board.start, []


def bfs(win: cs.window, board: Board):
    queue = [board.start]
    paths = [[board.start]]

    while len(queue) > 0:
        vpos = queue.pop(0)
        path = paths.pop(0).copy()

        update_and_draw(win, board, vpos, ".", 0)

        if board[vpos] == "G":
            return vpos, path[2:]

        moves = possible_moves(board, vpos)

        for move in moves:
            adjacent = vpos + move
            if board[adjacent] != "*":
                update_and_draw(win, board, adjacent, "*", 20)
                queue.append(adjacent)
                paths.append(path + [vpos])

    return board.start, []


def ucs(win: cs.window, board: Board):
    frontier = PQueue()
    expanded = []
    paths = {}

    frontier.update(board.start, 0)
    paths[board.start] = [board.start]

    while not frontier.empty():
        vpos, _ = frontier.min()
        path = paths.pop(vpos).copy()

        update_and_draw(win, board, vpos, ".", 0)

        if board[vpos] == "G":
            return vpos, path[2:]

        expanded.append(vpos)

        moves = possible_moves(board, vpos)
        for move in moves:
            adjacent = vpos + move
            cost = Coord.dist(adjacent, board.goal)
            if adjacent not in expanded and adjacent not in frontier:
                update_and_draw(win, board, adjacent, "*", 20)
                frontier.update(adjacent, cost)
                paths[adjacent] = path + [vpos]
            elif adjacent in frontier:
                if cost < frontier.get(adjacent):
                    frontier.update(adjacent, cost)


    return board.start, []


def a_star(win: cs.window, board: Board):
    frontier = PQueue()
    expanded = []
    paths = {}

    frontier.update(board.start, 0)
    paths[board.start] = [board.start]

    while not frontier.empty():
        vpos, _ = frontier.min()
        path = paths.pop(vpos).copy()

        update_and_draw(win, board, vpos, ".", 0)

        if board[vpos] == "G":
            return vpos, path[2:]

        expanded.append(vpos)

        moves = possible_moves(board, vpos)
        for move in moves:
            adjacent = vpos + move
            cost = Coord.dist(adjacent, board.goal)
            if adjacent not in expanded and adjacent not in frontier:
                update_and_draw(win, board, adjacent, "*", 20)
                frontier.update(adjacent, cost)
                paths[adjacent] = path + [vpos]
            elif adjacent in frontier:
                if cost < frontier.get(adjacent):
                    frontier.update(adjacent, cost)


    return board.start, []
