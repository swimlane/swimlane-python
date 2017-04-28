import pytest

from swimlane.core.resources import User


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
