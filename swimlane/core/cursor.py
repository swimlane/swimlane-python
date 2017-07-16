

class Cursor(object):

    def __init__(self, initial_elements=None):
        self._elements = initial_elements or []

    def __len__(self):
        return len(self._evaluate())

    def __iter__(self):
        for element in self._evaluate():
            yield element

    def __getitem__(self, item):
        return self._evaluate()[item]

    def _evaluate(self):
        """Hook to allow lazy evaluation or retrieval of cursor's elements

        Defaults to simply returning list of self._elements
        """
        return self._elements
