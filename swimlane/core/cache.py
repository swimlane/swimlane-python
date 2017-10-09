import copy
import functools
import logging
from collections import defaultdict

from cachetools import LFUCache

from swimlane.core.resources.base import APIResource


logger = logging.getLogger(__name__)


class ResourcesCache(object):
    """Universal APIResource instance cache

    Uses separate caches per APIResource type, and provides mapping between available cache keys and real cache
    primary key automatically

    .. versionadded:: 2.16.2
    """

    def __init__(self, per_cache_max_size):
        self.__cache_max_size = per_cache_max_size
        self.__caches = defaultdict(self.__cache_factory)
        self.__cache_key_map = {}

        if self.__cache_max_size == 0:
            logger.warning('Cache size set to 0, resource caching disabled')

    def __len__(self):
        """Return sum of all cache sizes"""
        return sum(c.currsize for c in self.__caches.values())

    def __getitem__(self, item):
        """Get cached resource, expects item to be 3-length tuple of (resource class, target key, target value)"""
        cls = item[0]

        # Check if in any fields index
        cache_internal_key = self.__cache_key_map[item]

        try:
            # Return copy of cached object
            return copy.copy(self.__caches[cls][cache_internal_key])
        except KeyError:
            # Internal cache miss for target resource, quietly remove from cache key map and let error bubble
            self.__cache_key_map.pop(item, None)
            raise

    def __delitem__(self, resource):
        """Remove resource instance from internal cache"""
        self.__caches[type(resource)].pop(resource.get_cache_internal_key(), None)

    def __cache_factory(self):
        """Build and return a new cache instance"""
        return LFUCache(self.__cache_max_size)

    def cache(self, resource):
        """Insert a resource instance into appropriate resource cache"""
        if self.__cache_max_size == 0:
            # Disable adding any resources to cache
            return

        resource_type = type(resource)

        if not isinstance(resource, APIResource):
            raise TypeError('Cannot cache type `{}`'.format(resource_type))

        try:
            cache_internal_key = resource.get_cache_internal_key()
            cache_index_keys = resource.get_cache_index_keys().items()
        except NotImplementedError:
            logger.warning(
                'Not caching `{!r}`, resource did not provide all necessary cache details'.format(resource)
            )
        else:
            for key, value in cache_index_keys:
                self.__cache_key_map[(resource_type, key, value)] = cache_internal_key

            self.__caches[type(resource)][cache_internal_key] = resource

            logger.debug('Cached `{!r}`'.format(resource))

    def clear(self, *resource_types):
        """Clear cache for each provided APIResource class, or all resources if no classes are provided"""
        resource_types = resource_types or tuple(self.__caches.keys())

        for cls in resource_types:
            # Clear and delete cache instances to guarantee no lingering references
            self.__caches[cls].clear()
            del self.__caches[cls]


def check_cache(resource_type):
    """Decorator for adapter methods to check cache for resource before normally sending requests to retrieve data

    Only works with single kwargs, almost always used with @one_of_keyword_only decorator
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                adapter = args[0]
                key, val = list(kwargs.items())[0]
            except IndexError:
                logger.warning("Couldn't generate full index key, skipping cache")
            else:

                index_key = (resource_type, key, val)
                try:
                    cached_record = adapter._swimlane.resources_cache[index_key]
                except KeyError:
                    logger.debug('Cache miss: {}'.format(index_key))
                else:
                    logger.debug('Cache hit: `{!r}`'.format(cached_record))
                    return cached_record

            # Fallback to default function call
            return func(*args, **kwargs)

        return wrapper
    return decorator
