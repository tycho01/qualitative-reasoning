from collections import Mapping

class FrozenDict(Mapping):
    """immutable hashable dict alternative"""

    def __init__(self, *args, **kwargs):
        self._d = dict(*args, **kwargs)
        self._hash = None

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __getitem__(self, key):
        return self._d[key]

    def items(self):
        return self._d.items()

    def __hash__(self):
        # It would have been simpler and maybe more obvious to 
        # use hash(tuple(sorted(self._d.items()))) from this discussion
        # so far, but this solution is O(n). I don't know what kind of 
        # n we are going to run into, but sometimes it's hard to resist the 
        # urge to optimize when it will gain improved algorithmic performance.
        if self._hash is None:
            self._hash = 0
            for pair in self.items():
                self._hash ^= hash(pair)
        return self._hash
