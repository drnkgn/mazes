import math

class Coord:
    def __init__(self, y=0, x=0):
        self.update(y, x)


    def __add__(self, other):
        copy = self.copy()
        copy.y = copy.y + other.y
        copy.x = copy.x + other.x

        return copy

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)


    def __ne__(self, other):
        return (self.x != other.x or self.y != other.y)


    def __str__(self):
        return f"{(self.x, self.y)}"


    def __hash__(self):
        return hash(f"{self.x}{self.y}")


    def update(self, y, x):
        self.y = y
        self.x = x


    def copy(self):
        return Coord(self.y, self.x)


    @staticmethod
    def dist(p, q):
        return math.sqrt((p.x - q.x)**2 + (p.y - q.y)**2)


class Board:
    def __init__(self, filepath, start="S", goal="G"):
        self.board = []
        self.start = Coord()
        self.goal = Coord()

        self.load(filepath, start, goal)


    def __str__(self):
        for row in self.board:
            print("".join(row))


    def __iter__(self):
        for row in self.board:
            yield row


    def __getitem__(self, pos: Coord):
        return self.board[pos.y][pos.x]


    def __setitem__(self, pos: Coord, value):
        self.board[pos.y][pos.x] = value


    def load(self, filepath, start, goal):
        with open(filepath, "r") as file:
            for row, line in enumerate(file):
                self.board.append(list(line.strip()))
                scol = line.find(start)
                ecol = line.find(goal)

                if scol > 0: self.start.update(row, scol)
                if ecol > 0: self.goal.update(row, ecol)

        self.width = len(self.board[0])
        self.height = len(self.board)


class PQueue:
    def __init__(self):
        self.map = {}


    def __contains__(self, item):
        return item in self.map


    def get(self, key):
        return self.map[key]

    
    def update(self, key, value):
        self.map[key] = value


    def min(self):
        mkey = min(self.map, key=self.map.get) # pyright: ignore

        return mkey, self.map.pop(mkey)


    def max(self):
        mkey = max(self.map, key=self.map.get) # pyright: ignore

        return mkey, self.map.pop(mkey)


    def empty(self):
        return len(self.map) == 0


    def insert(self, data, priority):
        self.map[data] = priority

