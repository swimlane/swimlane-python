import weakref


class APIResourceAdapter(object):
    """Base class for all API endpoint classes"""

    def __init__(self, swimlane):
        # Store weakref to swimlane to prevent circular reference and memory leak / Swimlane instance
        self.__refsw = weakref.ref(swimlane)

    @property
    def swimlane(self):
        """Resolve the swimlane weakref"""
        return self.__refsw()


class APIResource(object):
    """Base class for all API objects"""

    def __init__(self, swimlane, raw):
        self.swimlane = swimlane
        self._raw = raw

    def save(self):
        raise NotImplementedError
