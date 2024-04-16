class Coord:
    def __init__(self, y=0, x=0):
        self.set(y, x)


    def __add__(self, other):
        copy = self.copy()
        copy.y = copy.y + other.y
        copy.x = copy.x + other.x

        return copy


    def __str__(self):
        return f"{(self.x, self.y)}"


    def set(self, y=0, x=0):
        self.y = y
        self.x = x


    def copy(self):
        return Coord(self.y, self.x)


class Board:
    def __init__(self, filepath=""):
        self.board = []
        self.start = Coord()

        if filepath != "":
            self.load(filepath)


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


    def load(self, filepath):
        with open(filepath, "r") as file:
            for row, line in enumerate(file):
                self.board.append(list(line.strip()))
                col = line.find("S")

                if line.find("S") > 0:
                    self.start.set(row, col)
