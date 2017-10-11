import pytest

from swimlane.core.resources.usergroup import User
from swimlane.core.resources.base import APIResource


def test_repr(mock_user):
    """Use User resource to test base __repr__"""
    assert repr(mock_user) == '<User: admin>'


@pytest.mark.parametrize('raw', [
    {},
    {'$type': 'Wrong Type'}
])
def test_type_checks(mock_swimlane, raw):
    """Use User class to test $type validation"""
    with pytest.raises(TypeError):
        User(mock_swimlane, raw)


def test_base_no_default_cache_index_keys(mock_swimlane):
    r = APIResource(mock_swimlane, {})

    with pytest.raises(NotImplementedError):
        r.get_cache_index_keys()
