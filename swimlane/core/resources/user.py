"""This module provides a User class."""

from ..auth import Client
from .resource import Resource


class User(Resource):
    """A class for working with Swimlane users."""

    def __init__(self, fields):
        """Init a User with fields.

        Args:
            fields (dict): A dict of fields and values.
        """
        super(User, self).__init__(fields)

    @classmethod
    def find_all(cls):
        """List all users.

        Returns:
            A generator that yields all users in the system.
        """
        return (User(u) for u in Client.get("user").get('users', []))

    @classmethod
    def find(cls, user_id=None, name=None):
        """Find users.

        Args:
            user_id (str): The user ID.
            name (str): A name or a fragment of a name to search by.

        Returns:
            A single User if user_id was specified, otherwise a generator
            that yields Users for all system users who's username matched.
        """
        if user_id:
            return User(Client.get("user/{0}".format(user_id)))

        return (User(u) for u
                in Client.get("user/search?query={0}".format(name)))
