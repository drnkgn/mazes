from .board import Board
import curses as cs
import time
import algo
import os
import psutil

class Renderer:
    def __init__(self, puzzle, solver):
        if os.path.isfile(puzzle):
            self.board = Board(puzzle)
        else:
            print(f"Error: file '{puzzle}' does not exists")
            exit()

        if solver in ["dfs", "bfs", "greedy", "ucs", "a_star"]:
            self.solver = getattr(algo, solver)
        else:
            print(f"Error: solver '{solver}' unknown")
            exit()


    def init_color(self):
        cs.init_pair(1, cs.COLOR_RED, cs.COLOR_BLACK)
        cs.init_pair(2, cs.COLOR_GREEN, cs.COLOR_BLACK)
        cs.init_pair(3, cs.COLOR_BLACK, 215)
        cs.init_pair(4, cs.COLOR_WHITE, cs.COLOR_BLACK)
        cs.init_pair(5, 237, cs.COLOR_BLACK)
        cs.init_pair(6, cs.COLOR_WHITE, cs.COLOR_WHITE)


    def init_win(self):
        self.win = dict(
            board=cs.newwin(self.board.height+1, cs.COLS, 0, 0),
            debug=cs.newwin(10, cs.COLS, self.board.height+2, 0)
        )


    def main(self, stdscr: cs.window):
        cs.start_color()
        cs.use_default_colors()
        cs.curs_set(0)

        self.init_win()
        self.init_color()

        for i, row in enumerate(self.board):
            for e in row:
                if e == "█":
                    self.win["board"].addch(" ", cs.color_pair(6))
                else:
                    self.win["board"].addch(e, cs.color_pair(4))

            if "S" in row:
                self.win["board"].move(i, row.index("S"))
                self.win["board"].addch("█", cs.color_pair(2))
            if "G" in row:
                self.win["board"].move(i, row.index("G"))
                self.win["board"].addch("█", cs.color_pair(1))

            self.win["board"].move(i+1, 0)


        self.win["board"].refresh()

        self.win["debug"].addstr("Press any key to continue...")
        self.win["debug"].getkey()
        self.win["debug"].move(0, 0)
        self.win["debug"].addstr("                            ")
        self.win["debug"].refresh()

        start = time.time()
        goal, paths, states = self.solver(self.win["board"], self.board)
        mem = psutil.Process(os.getpid()).memory_info().rss / 1024 /1024
        end = time.time()

        for path in paths:
            self.win["board"].move(path.y, path.x)
            self.win["board"].addch("•", cs.color_pair(3))

        self.win["board"].refresh()

        self.win["debug"].move(1, 0)
        self.win["debug"].addstr(f"Goal found at   : {goal}\n")
        self.win["debug"].addstr(f"Number of states: {states}\n")
        self.win["debug"].addstr(f"Time taken      : {end - start:.2f} s\n")
        self.win["debug"].addstr(f"Mem usage       : {mem:.2f} MB\n")
        self.win["debug"].addstr(f"Path length     : {len(paths)}\n")
        self.win["debug"].refresh()

        self.win["debug"].getkey()
