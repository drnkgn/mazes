import math

class Coord:
    """A 2D coordinate class."""
    def __init__(self, y=0, x=0):
        self.update(y, x)


    def __add__(self, other):
        """Adds two coordinates and returns a **copy** as result."""
        copy = self.copy()
        copy.y = copy.y + other.y
        copy.x = copy.x + other.x

        return copy

    def __eq__(self, other):
        """Checks equality of two coordinates"""
        return (self.x == other.x and self.y == other.y)


    def __ne__(self, other):
        """Checks inequality of two coordinates"""
        return (self.x != other.x or self.y != other.y)


    def __str__(self):
        """
        Represents the coordinate as a `string` so that it can be printed
        easily.
        """
        return f"{(self.x, self.y)}"


    def __hash__(self):
        """
        Computes a unique hash for the coordinate for storing in hash maps.
        """
        return hash(f"{self.x}{self.y}")


    def update(self, y, x):
        """Updates the coordinate."""
        self.y = y
        self.x = x


    def copy(self):
        """Returns a copy of itself."""
        return Coord(self.y, self.x)


    @staticmethod
    def dist(p, q):
        """Computes the Manhattan distance between two coordinates."""
        return abs(p.x - q.x) + (p.y - q.y)


class Board:
    def __init__(self, filepath,
                 wall="█", start="S", goal="G", discovered="*", expanded="•"):
        self.board = []
        self.start = Coord()
        self.goal = Coord()
        self.icon = dict(
            wall=wall,
            start=start,
            goal=goal,
            discovered=discovered,
            expanded=expanded
        )

        self.load(filepath, start, goal)


    def __str__(self):
        """
        Represents the board as a `string` so that it can be printed easily.
        """
        for row in self.board:
            print("".join(row))


    def __iter__(self):
        """Iterator that iterates through the rows of the board."""
        for row in self.board:
            yield row


    def __getitem__(self, pos: Coord):
        """
        Used to access the board's cell via the [] operator, e.g.:

        ```python
            print(board[pos])
        ```
        """
        return self.board[pos.y][pos.x]


    def __setitem__(self, pos: Coord, value):
        """
        Used to set the board's cell via the [] operator, e.g.:

        ```python
            board[pos] = something_else
        ```
        """
        self.board[pos.y][pos.x] = value


    def adjacent(self, current: Coord):
        """
        Returns an interator of undiscovered adjacent nodes from the
        current node.
        """
        return BoardAdjacentIterator(self, current)


    def isgoal(self, node: Coord):
        """
        Checks if node is goal.
        """
        return self[node] == self.icon["goal"]


    def discovered(self, node: Coord):
        """
        Checks if node is discovered (i.e., reached but not checked).
        """
        return self[node] == self.icon["discovered"]


    def expanded(self, node: Coord):
        """
        Checks if node is expanded (i.e., has been checked).
        """
        return self[node] == self.icon["expanded"]


    def load(self, filepath, start, goal):
        """Loads a board from a file."""
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
    """A really shitty implementation of a priority queue..."""
    def __init__(self):
        self.map = {}


    def __contains__(self, key):
        """
        Test an element's existance within the PQueue via `in` keyword, e.g.,

        ```python
            queue = PQueue()
            queue.insert("a", 3)
            print("a" in queue)
        ```
        """
        return key in self.map


    def get(self, key):
        """Returns the priority of the element."""
        return self.map[key]


    def update(self, data, priority):
        """Updates the priority of an element in the queue."""
        self.map[data] = priority


    def min(self):
        """Returns and removes the element with the lowest priority."""
        key = min(self.map, key=self.map.get) # pyright: ignore

        return key, self.map.pop(key)


    def max(self):
        """Returns and removes the element with the highest priority."""
        key = max(self.map, key=self.map.get) # pyright: ignore

        return key, self.map.pop(key)


    def empty(self):
        """Test the emptiness of the queue."""
        return len(self.map) == 0


class BoardAdjacentIterator:
    def __init__(self, board: Board, current: Coord):
        self.adjacent = self.possible_moves_(board, current)


    def __iter__(self):
        for node in self.adjacent:
            yield node


    def possible_moves_(self, board: Board, current: Coord) -> list[Coord]:
        """
        Returns a list of possible from the current position.
        """
        moves = []

        if board[current + Coord(0, 1)] not in ("█", "•", "S"):
            moves.append(current + Coord(0, 1))

        if board[current + Coord(1, 0)] not in ("█", "•", "S"):
            moves.append(current + Coord(1, 0))

        if board[current + Coord(0, -1)] not in ("█", "•", "S"):
            moves.append(current + Coord(0, -1))

        if board[current + Coord(-1, 0)] not in ("█", "•", "S"):
            moves.append(current + Coord(-1, 0))

        return moves

