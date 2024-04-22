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


    def update(self, data, priority):
        """Updates the priority of an element in the queue."""
        self.map[data] = priority


    def pop(self):
        """Returns and removes the element with the lowest priority."""
        key = min(self.map, key=self.map.get) # pyright: ignore

        return key, self.map.pop(key)


    def empty(self):
        """Test the emptiness of the queue."""
        return len(self.map) == 0


class PStack(PQueue):
    """
    An even shitier implementation of PQueue that behaves like a stack for
    elements with equal priority...
    """

    def __init__(self):
        super().__init__()


    def pop(self):
        flatten = list(self.map.items())
        flatten.reverse()
        key, _ = min(flatten, key=lambda x: x[1])

        return key, self.map.pop(key)
