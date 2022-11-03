import six

from swimlane.core.resolver import SwimlaneResolver
from typing import Dict, Any


class APIResourceMetaclass(type):
    """Metaclass for all APIResource classes"""

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Hook __init__ call to push resource instance into Swimlane client ResourceCache after instantiation"""
        resource_instance = type.__call__(cls, *args, **kwargs)

        resource_instance._swimlane.resources_cache.cache(resource_instance)

        return resource_instance


class APIResource(six.with_metaclass(APIResourceMetaclass, SwimlaneResolver)):
    """Base class for all API resources with an associated $type and/or raw data"""

    _type = None

    def __init__(self, swimlane: Any, raw: Any) -> None:
        super(APIResource, self).__init__(swimlane)
        self._raw = raw

        raw_type = self._raw.get('$type')
        if self._type and raw_type != self._type:
            raise TypeError('Expected $type = "{}", received "{}"'.format(self._type, raw_type))

    def __repr__(self) -> str:
        return '<{self.__class__.__name__}: {self!s}>'.format(self=self)

    def __str__(self) -> str:
        return ''

    def __hash__(self) -> int:
        """Added for py2+3 compat"""
        return int(id(self) / 16)

    def __eq__(self, other: Any) -> bool:
        """Determine if an APIResource is of the same type and has the same hash value"""
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __ne__(self, other: Any) -> bool:
        # Default __ne__ for python 2 compat
        return not self == other

    def get_cache_internal_key(self) -> int:
        """Return real internal cache key for resource instance"""
        return hash(self)

    def get_cache_index_keys(self) -> Dict[Any, Any]:
        """Return dict of key/value pairs used by ResourceCache to map resource values to internal cache instance"""
        raise NotImplementedError
