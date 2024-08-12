from utils.renderer import Renderer
import curses as cs
import sys
import os

if __name__ == "__main__":
    usage = (
"""Usage: python main.py <puzzle_file> <algorithm>
            puzzle_file     The file that contains the puzzle. The
                            following shows the ascii representation in
                            the puzzle file:
                                "█"             wall
                                " "             valid path
                                "S"             start position
                                "G"             goal position

                            The following shows the ascii representation in
                            the solution:
                                "*"             explored path
                                "#"             found path

            algorithm       The algorithm used to solve the maze puzzle.
                            Must be one of the following:
                                dfs, bfs, greedy, ucs, a_star"""
)

    if len(sys.argv) != 3:
        print("Error: wrong argument given")
        print(usage)
    else:
        if not os.path.isfile(sys.argv[1]):
            print(f"Error: file {sys.argv[1]} not found")
            exit()

        if sys.argv[2] not in ["dfs", "bfs", "greedy", "ucs", "a_star"]:
            print(f"Error: unknown algorithm '{sys.argv[2]}'")
            print(usage)
            exit()

    renderer = Renderer(sys.argv[1], sys.argv[2])
    cs.wrapper(renderer.main)
