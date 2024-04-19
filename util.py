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
        """Computes the Euclidean distance between two coordinates."""
        return math.sqrt((p.x - q.x)**2 + (p.y - q.y)**2)


class Board:
    def __init__(self, filepath, start="S", goal="G"):
        self.board = []
        self.start = Coord()
        self.goal = Coord()

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
        mkey = min(self.map, key=self.map.get) # pyright: ignore

        return mkey, self.map.pop(mkey)


    def max(self):
        """Returns and removes the element with the highest priority."""
        mkey = max(self.map, key=self.map.get) # pyright: ignore

        return mkey, self.map.pop(mkey)


    def empty(self):
        """Test the emptiness of the queue."""
        return len(self.map) == 0
