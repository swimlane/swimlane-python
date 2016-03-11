import unittest

from swimlane.core.resources import User


class UserTestCase(unittest.TestCase):
    pass

"""
USER_ID = "5674909d55d95d5c30d02200"


def test_find_all(default_client):
    users = list(User.find_all())
    assert len(users) > 0
    assert any(u.isMe for u in users)


def test_find_by_id(default_client):
    user = User.find(user_id=USER_ID)
    assert user
    assert user.isMe
    assert user.userName == "admin"


def test_find_by_name(default_client):
    users = list(User.find(name="sam"))
    assert users
    assert len(users) == 1
    sam = users[0]
    assert sam
    assert not sam.disabled
    assert sam.name == "sspade"


def test_find_multiple_by_name(default_client):
    users = list(User.find(name="a"))
    assert len(users) == 2
"""
