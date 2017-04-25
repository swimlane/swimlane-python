import weakref


class SwimlaneResolver(object):
    """Provides automatic weakref resolution for Swimlane client to avoid circular references and memory leaks"""

    def __init__(self, swimlane):
        self.__ref_swimlane = weakref.ref(swimlane)

    @property
    def _swimlane(self):
        """Transparently resolve the swimlane weakref"""
        return self.__ref_swimlane()


class APIResource(SwimlaneResolver):
    """Base class for all API resources with an associated $type and/or raw data"""

    _type = None

    def __init__(self, swimlane, raw):
        super(APIResource, self).__init__(swimlane)
        self._raw = raw

        if self._type and self._raw['$type'] != self._type:
            raise TypeError('Expected $type = "{}", received "{}"'.format(self._type, self._raw['$type']))

    def __repr__(self):
        return '<{self.__class__.__name__}: {self!s}>'.format(self=self)
