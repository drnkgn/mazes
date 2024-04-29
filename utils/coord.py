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

