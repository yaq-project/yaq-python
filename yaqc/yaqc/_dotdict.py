from collections.abc import Mapping


class DotDict(Mapping):
    """A simple mapping allowing dot notation."""

    def __init__(self, **kwargs):
        self._dict = kwargs
        for k, v in self._dict.items():
            setattr(self, k, v)

    def __getitem__(self, name):
        return self._dict[name]

    def __setitem__(self, k, v):
        self._dict[k] = v
        setattr(self, k, v)

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)
