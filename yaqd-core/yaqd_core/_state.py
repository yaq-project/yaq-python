"""Special class for saving state. A dictonary with attribute 'updated'."""


class State(dict):
    def __init__(self, *args, **kwargs):
        """A dictionary with special attribute 'updated'.
        Internal behavior will never set updated to False.
        """
        super().__init__(*args, **kwargs)
        self.updated = True

    def __setitem__(self, item, value):
        super().__setitem__(item, value)
        self.updated = True

    def update(self, iterable):
        super().update(iterable)
        self.updated = True
