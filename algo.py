from utils.coord import Coord
from utils.board import Board
from utils.pqueue import PQueue, PStack
import curses as cs
import math


def update_and_draw(win: cs.window,
                    board: Board,
                    pos: Coord,
                    char: str,
                    ms: int) -> None:
    """
    Updates position on the board as visited both internally and during the
    animation.
    """
    if pos != board.goal and pos != board.start:
        board[pos] = char

        win.move(pos.y, pos.x)
        win.addch(char, cs.color_pair(4))
        win.refresh()
        cs.napms(ms)


def dfs(win: cs.window, board: Board):
    stack = [board.start]
    paths = [[board.start]]
    state = 0

    while len(stack) > 0:
        current = stack.pop()
        path = paths.pop().copy()

        update_and_draw(win, board, current, "•", 0)

        if current == board.goal:
            return current, path[2:], state

        for neighbour in board.adjacent(current):
            if board[neighbour] != "*":
                update_and_draw(win, board, neighbour, "*", 5)
                stack.append(neighbour)
                paths.append(path + [current])

                state = state + 1

    return board.start, [], state


def bfs(win: cs.window, board: Board):
    queue = [board.start]
    paths = [[board.start]]
    state = 0

    while len(queue) > 0:
        current = queue.pop(0)
        path = paths.pop(0).copy()

        update_and_draw(win, board, current, "•", 0)

        if current == board.goal:
            return current, path[2:], state

        for neighbour in board.adjacent(current):
            if board[neighbour] != "*":
                update_and_draw(win, board, neighbour, "*", 5)
                queue.append(neighbour)
                paths.append(path + [current])

                state = state + 1

    return board.start, [], state


def greedy(win: cs.window, board: Board):
    frontier = PQueue()
    expanded = []
    paths = {}
    state = 0

    frontier.update(board.start, 0)
    paths[board.start] = [board.start]

    while not frontier.empty():
        current, _ = frontier.pop()
        path = paths.pop(current)

        update_and_draw(win, board, current, "•", 0)

        if current == board.goal:
            return current, path[2:], state

        expanded.append(current)

        for neighbour in board.adjacent(current):
            cost = Coord.dist(neighbour, board.goal)

            if neighbour not in expanded:
                update_and_draw(win, board, neighbour, "*", 5)
                frontier.update(neighbour, cost)
                paths[neighbour] = path + [current]
                state = state + 1

    return board.start, [], state


def ucs(win: cs.window, board: Board):
    states = 0
    g_score = {}
    open_set = PQueue()
    paths = {}

    g_score[board.start] = 0
    open_set.update(board.start, 0)
    paths[board.start] = [board.start]

    while not open_set.empty():
        current, _ = open_set.pop()
        path = paths.pop(current)

        update_and_draw(win, board, current, "•", 0)

        if current == board.goal:
            return current, path[2:], states

        for neighbour in board.adjacent(current):
            tentative = g_score[current] + Coord.dist(current, neighbour)

            if tentative < g_score.get(neighbour, math.inf):
                g_score[neighbour] = tentative

                if neighbour not in open_set:
                    update_and_draw(win, board, current, "*", 5)

                    open_set.update(neighbour, g_score[neighbour])
                    paths[neighbour] = path + [current]

                    states = states + 1

    return board.start, [], states


def a_star(win: cs.window, board: Board):
    def heuristic(node: Coord):
        return Coord.dist(node, board.goal)

    open_set = PStack()
    g_score = {}
    f_score = {}
    paths = {}
    states = 0

    g_score[board.start] = 0
    f_score[board.start] = heuristic(board.start)
    open_set.update(board.start, f_score[board.start])
    paths[board.start] = [board.start]

    while not open_set.empty():
        current, _ = open_set.pop()
        path = paths.pop(current)

        update_and_draw(win, board, current, "•", 0)

        if current == board.goal:
            return current, path[2:], states

        for neighbour in board.adjacent(current):
            tentative = g_score[current] + Coord.dist(current, neighbour)

            if tentative < g_score.get(neighbour, math.inf):
                g_score[neighbour] = tentative
                f_score[neighbour] = tentative + heuristic(neighbour)

                if neighbour not in open_set:
                    update_and_draw(win, board, neighbour, "*", 5)

                    open_set.update(neighbour, f_score[neighbour])
                    paths[neighbour] = path + [current]

                    states = states + 1

    return board.start, [], states
