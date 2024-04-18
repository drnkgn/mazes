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
