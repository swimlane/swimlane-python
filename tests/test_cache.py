"""Tests for the ResourceCache class"""

import copy

import mock
import pytest

from swimlane.core.cache import ResourcesCache, check_cache
from swimlane.core.resources.base import APIResource
from swimlane.core.resources.record import Record


def test_len(mock_app, mock_record):
    """Test cache length includes all cached resources"""

    cache = ResourcesCache(10)

    assert len(cache) == 0

    cache.cache(mock_app)
    assert len(cache) == 1

    # Ignore duplicates
    cache.cache(mock_app)
    assert len(cache) == 1

    cache.cache(mock_record)
    assert len(cache) == 2


def test_separate_resource_caches(mock_app, mock_record):
    """Test each resource class has a separate queue of max size instead of a single global queue"""

    # Max cache size of 1 per resource type
    cache = ResourcesCache(1)

    cache.cache(mock_app)
    cache.cache(mock_record)

    assert len(cache) == 2

    # Create another record instance
    other_record = copy.copy(mock_record)
    other_record.id = mock_record.id + '123'

    # Check that only one record is still in the cache
    cache.cache(other_record)
    assert len(cache) == 2


def test_item_in_cache(mock_record):
    """Test checking if item exists in cache"""

    cache = ResourcesCache(5)

    assert mock_record not in cache

    cache.cache(mock_record)

    assert mock_record in cache


def test_get_item_from_cache(mock_record):
    """Test retrieving item from cache, and that item is a copy instead of reference to same instance"""

    cache = ResourcesCache(5)

    cache_key = (type(mock_record), 'id', mock_record.id)

    # Attempt to get before record is in cache
    with pytest.raises(KeyError):
        cached_record = cache[cache_key]

    cache.cache(mock_record)

    cached_record = cache[cache_key]

    assert cached_record == mock_record
    assert cached_record is not mock_record

    # Prove failure after clearing cache
    cache.clear()
    with pytest.raises(KeyError):
        cached_record = cache[cache_key]


def test_clear(mock_app, mock_record):
    """Test clearing individual and all resources from cache"""

    cache = ResourcesCache(5)

    cache.cache(mock_app)
    cache.cache(mock_record)

    assert len(cache) == 2

    # Clear by resource class type
    cache.clear(type(mock_app))

    assert len(cache) == 1
    assert mock_app not in cache
    assert mock_record in cache

    cache.cache(mock_app)

    assert len(cache) == 2

    # Clear all caches
    cache.clear()

    assert len(cache) == 0
    assert mock_app not in cache
    assert mock_record not in cache


def test_check_cache_decorator(mock_swimlane, mock_record):
    """Check that decorator prevents actual function call on cache hits and defers to normal call on cache misses"""

    expected_miss_sentinel = object()

    mock_func = mock.MagicMock()
    mock_func.return_value=expected_miss_sentinel
    mock_func.__name__ = 'mock_func'
    decorated_func = check_cache(Record)(mock_func)

    mock_adapter = mock.MagicMock()
    mock_swimlane.resources_cache = ResourcesCache(5)
    mock_adapter._swimlane = mock_swimlane

    # Record not in cache yet, should call the actual mock_func with original inputs
    assert decorated_func(mock_adapter, id=mock_record.id) is expected_miss_sentinel
    mock_func.assert_called_once_with(mock_adapter, id=mock_record.id)

    # Record is returned from cache, shouldn't call the actual mock_func again
    mock_swimlane.resources_cache.cache(mock_record)
    assert decorated_func(mock_adapter, id=mock_record.id) == mock_record
    assert mock_func.call_count == 1


def test_unsupported_api_resource_instance(mock_swimlane):
    """Test that APIResource instances not returning all cache details are ignored but don't fail"""
    cache = ResourcesCache(5)

    cache.cache(APIResource(mock_swimlane, {}))

    assert len(cache) == 0


@pytest.mark.parametrize('item', [
    object(),
    None,
    {},
    [],
    'string',
    123
])
def test_cache_unsupported_type(item):
    """Test attempting to cache a non-APIResource instance fails"""
    cache = ResourcesCache(5)

    with pytest.raises(TypeError):
        cache.cache(item)


@pytest.mark.parametrize('key', [
    object(),
    None,
    {},
    [],
    (),
    ('string', 'wrong_leading_type', 'value'),
    (object, 'wrong_leading_type', 'value'),
    (Record, 'wrong_length'),
    (Record, 'wrong_length', 'wrong_length', 'wrong_length'),
])
def test_cache_invalid_index_key(key):
    """Test exception raised when attempting lookup with invalid index key"""
    cache = ResourcesCache(5)

    with pytest.raises(TypeError):
        item = cache[key]
