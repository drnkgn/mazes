from utils.renderer import Renderer
import curses as cs
import sys

if __name__ == "__main__":
    renderer = Renderer(sys.argv[1], sys.argv[2])
    cs.wrapper(renderer.main)
