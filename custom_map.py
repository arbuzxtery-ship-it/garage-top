from models import Entity


class CustomMap(Entity):
    """Замена словарю: пары [ключ, значение] хранятся в обычном списке"""

    def __init__(self):
        self._pairs = []

    def _find(self, key):
        for pair in self._pairs:
            if pair[0] == key:
                return pair
        return None

    def get(self, key, default=None):
        pair = self._find(key)
        if pair is None:
            return default
        return pair[1]

    def keys(self):
        return [pair[0] for pair in self._pairs]

    def values(self):
        return [pair[1] for pair in self._pairs]

    def items(self):
        return [(pair[0], pair[1]) for pair in self._pairs]

    def info(self):
        return f"CustomMap, элементов: {len(self)}"

    def __getitem__(self, key):
        pair = self._find(key)
        if pair is None:
            raise KeyError(key)
        return pair[1]

    def __setitem__(self, key, value):
        pair = self._find(key)
        if pair is None:
            self._pairs.append([key, value])
        else:
            pair[1] = value

    def __delitem__(self, key):
        pair = self._find(key)
        if pair is None:
            raise KeyError(key)
        self._pairs.remove(pair)

    def __contains__(self, key):
        return self._find(key) is not None

    def __len__(self):
        return len(self._pairs)

    def __iter__(self):
        return iter(self.keys())

    def __eq__(self, other):
        return isinstance(other, CustomMap) and self.items() == other.items()

    def __lt__(self, other):
        return len(self) < len(other)

    def __gt__(self, other):
        return len(self) > len(other)

    def __repr__(self):
        return f"CustomMap({self.items()})"

    def __str__(self):
        return ", ".join(f"{key}: {value}" for key, value in self.items())
