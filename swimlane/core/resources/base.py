import weakref


class APIResourceAdapter(object):
    """Base class for all API endpoint classes"""

    def __init__(self, swimlane):
        self.__ref_swimlane = weakref.ref(swimlane)

    @property
    def _swimlane(self):
        """Resolve the swimlane weakref"""
        return self.__ref_swimlane()


class APIResource(object):
    """Base class for all API objects"""

    _type = None

    def __init__(self, swimlane, raw):
        self._swimlane = swimlane
        self._raw = raw

        if self._type and self._raw['$type'] != self._type:
            raise TypeError('Expected $type = "{}", received "{}"'.format(self._type, self._raw['$type']))

    def __repr__(self):
        return '<{self.__class__.__name__}: {self}>'.format(self=self)

    def save(self):
        raise NotImplementedError

    def permalink(self):
        """Returns full URL to individual resource in Swimlane"""
        raise NotImplementedError
