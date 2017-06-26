from swimlane.core.resolver import SwimlaneResolver


class APIResource(SwimlaneResolver):
    """Base class for all API resources with an associated $type and/or raw data"""

    _type = None

    def __init__(self, swimlane, raw):
        super(APIResource, self).__init__(swimlane)
        self._raw = raw

        _raw_type = self._raw.get('$type')
        if self._type and _raw_type != self._type:
            raise TypeError('Expected $type = "{}", received "{}"'.format(self._type, _raw_type))

    def __repr__(self):
        return '<{self.__class__.__name__}: {self!s}>'.format(self=self)

    def __ne__(self, other):
        # Default __ne__ for python 2 compat
        return not self == other
