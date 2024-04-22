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


    def nmin(self, n):
        temp = list(self.map.items())
        temp = sorted(temp, key=lambda x: x[1]) # pyright: ignore

        ret = []
        for i in range(n):
            if i < len(temp):
                ret.append(temp[i])
            else:
                break

        return ret


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


    def get_min(self):
        flatten = list(self.map.items())
        flatten.reverse()
        key, _ = min(flatten, key=lambda x: x[1])

        return key, self.map.pop(key)
