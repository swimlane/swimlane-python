import weakref


class APIResourceAdapter(object):
    """Base class for all API endpoint classes"""

    def __init__(self, swimlane):
        self.__refsw = weakref.ref(swimlane)

    @property
    def swimlane(self):
        """Resolve the swimlane weakref"""
        return self.__refsw()


class APIResource(object):
    """Base class for all API objects"""

    _type = None

    def __init__(self, swimlane, raw):
        self.swimlane = swimlane
        self._raw = raw

        if self._type and self._raw['$type'] != self._type:
            raise TypeError('Expected $type = "{}", received "{}"'.format(self._type, self._raw['$type']))

    def save(self):
        raise NotImplementedError
