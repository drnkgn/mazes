from util import Coord, Board, PQueue
import curses as cs
import string

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
        win.addch(char, cs.color_pair(4))
        win.refresh()
        cs.napms(ms)


def dfs(win: cs.window, board: Board):
    """
    Returns the goal position and the path that that the algorithm traced.
    """
    stack = [board.start]
    paths = [[board.start]]
    state = 0

    while len(stack) > 0:
        current = stack.pop()
        path = paths.pop().copy()

        update_and_draw(win, board, current, "•", 0)

        if board.isgoal(current) == "G":
            return current, path[2:], state

        for adjacent in board.adjacent(current):
            if not board.discovered(current):
                update_and_draw(win, board, adjacent, "*", 20)
                stack.append(adjacent)
                paths.append(path + [current])

                state = state + 1

    return board.start, [], state


def bfs(win: cs.window, board: Board):
    """
    Returns the goal position and the path that that the algorithm found.
    """
    queue = [board.start]
    paths = [[board.start]]
    state = 0

    while len(queue) > 0:
        current = queue.pop(0)
        path = paths.pop(0).copy()

        update_and_draw(win, board, current, "•", 0)

        if board.isgoal(current):
            return current, path[2:], state

        for adjacent in board.adjacent(current):
            if not board.discovered(adjacent):
                update_and_draw(win, board, adjacent, "*", 20)
                queue.append(adjacent)
                paths.append(path + [current])

                state = state + 1

    return board.start, [], state


def greedy(win: cs.window, board: Board):
    """
    Returns the goal position and the path that that the algorithm traced. If
    the board does not include the cost, i.e., numbers from 0-9, then A*
    defaults to using Euclidean distance for the cost. Otherwise, A* will
    combine the costs and the distance from the goal as the determining cost.

    For boards without costs, e.g., puzzle 1-5, both UCS and A* works exactly
    the same.
    """
    frontier = PQueue()
    expanded = []
    paths = {}
    state = 0

    frontier.update(board.start, 0)
    paths[board.start] = [board.start]

    while not frontier.empty():
        current, _ = frontier.min()
        path = paths.pop(current).copy()

        update_and_draw(win, board, current, "•", 0)

        if board.isgoal(current):
            return current, path[2:], state

        expanded.append(current)

        for adjacent in board.adjacent(current):
            cost = 0

            if board[adjacent] in string.digits:
                cost = float(board[adjacent])

            if adjacent not in expanded and not board.discovered(adjacent):
                update_and_draw(win, board, adjacent, "*", 20)
                frontier.update(adjacent, cost)
                paths[adjacent] = path + [current]
                state = state + 1

    return board.start, [], state


def ucs(win: cs.window, board: Board):
    """
    Returns the goal position and the path that that the algorithm traced. If
    the board does not include the cost, i.e., numbers from 0-9, then UCS
    defaults to using Euclidean distance for the cost.

    For boards without costs or have the same costs throughout, both UCS
    works almost the same as BFS.
    """
    frontier = PQueue()
    expanded = []
    paths = {}
    state = 0

    frontier.update(board.start, 0)
    paths[board.start] = [board.start]

    while not frontier.empty():
        current, _ = frontier.min()
        path = paths.pop(current).copy()

        update_and_draw(win, board, current, "•", 0)

        if board.isgoal(current):
            return current, path[2:], state

        expanded.append(current)

        for adjacent in board.adjacent(current):
            cost = len(path)

            if board[adjacent] in string.digits:
                cost = cost + float(board[adjacent])

            if adjacent not in expanded and adjacent not in frontier:
                update_and_draw(win, board, adjacent, "*", 20)
                frontier.update(adjacent, cost)
                paths[adjacent] = path + [current]
                state = state + 1

    return board.start, [], state


def a_star(win: cs.window, board: Board):
    """
    Returns the goal position and the path that that the algorithm traced. If
    the board does not include the cost, i.e., numbers from 0-9, then A*
    defaults to using Euclidean distance for the cost. Otherwise, A* will
    combine the costs and the distance from the goal as the determining cost.

    For boards without costs, e.g., puzzle 1-5, both UCS and A* works exactly
    the same.
    """
    frontier = PQueue()
    expanded = []
    paths = {}
    state = 0
    cost = 0

    frontier.update(board.start, 0)
    paths[board.start] = [board.start]

    while not frontier.empty():
        current, _ = frontier.min()
        path = paths.pop(current).copy()

        update_and_draw(win, board, current, "•", 0)

        if board.isgoal(current):
            return current, path[2:], state

        expanded.append(current)

        for adjacent in board.adjacent(current):
            cost = len(path) + Coord.dist(adjacent, board.goal)

            if board[adjacent] in string.digits:
                cost = cost + float(board[adjacent])

            if adjacent not in expanded and not board.discovered(adjacent):
                update_and_draw(win, board, adjacent, "*", 20)
                frontier.update(adjacent, cost)
                paths[adjacent] = path + [current]
                state = state + 1

    return board.start, [], state


def naive(win: cs.window, board: Board):
    frontier = PQueue()
    expanded = []
    paths = {}
    state = 0
    cost = 0

    frontier.update(board.start, 0)
    paths[board.start] = [board.start]

    while not frontier.empty():
        current, _ = frontier.min()
        path = paths.pop(current).copy()

        update_and_draw(win, board, current, "•", 0)

        if board.isgoal(current):
            return current, path[2:], state

        expanded.append(current)

        for adjacent in board.adjacent(current):
            cost = Coord.dist(adjacent, board.goal)

            if board[adjacent] in string.digits:
                cost = cost + float(board[adjacent])

            if adjacent not in expanded and not board.discovered(adjacent):
                update_and_draw(win, board, adjacent, "*", 20)
                frontier.update(adjacent, cost)
                paths[adjacent] = path + [current]
                state = state + 1

    return board.start, [], state
