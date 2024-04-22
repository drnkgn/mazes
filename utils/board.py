from coord import Coord

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

