import pytest

from swimlane.core.cursor import Cursor, PaginatedCursor


def test_cursor_iteration():
    cursor = Cursor()
    cursor._elements = range(5)

    for idx, cursor_idx in zip(range(5), cursor):
        assert idx == cursor_idx


def test_cursor_len():
    cursor = Cursor()
    cursor._elements = range(5)

    assert len(cursor) == 5


def test_paginated_cursor_hooks():
    cursor = PaginatedCursor()

    # Default raises exception
    with pytest.raises(NotImplementedError):
        cursor._retrieve_raw_elements(0)

    # Noop parse hook
    assert cursor._parse_raw_element(1) == 1
