"""This module provides a Group class."""

from ..auth import Client
from .resource import Resource


class Group(Resource):
    """A class for working with Swimlane groups."""

    def __init__(self, fields):
        """Init a Group with fields.

        Args:
            fields (dict): A dict of fields and values.
        """
        super(Group, self).__init__(fields)

    @classmethod
    def find_all(cls):
        """Get all groups.

        Returns:
            A generator that yields all groups in the system.
        """
        return (Group(g) for g in Client.get("groups").get('groups', []))

    @classmethod
    def find(cls, group_id=None, name=None):
        """Find groups.

        Args:
            group_id (str): The group ID.
            name (str): A name or a fragment of a name to search by.

        Returns:
            A single Group if group_id was specified, otherwise a generator
            that yields Groups for all system groups with matching names..
        """
        if group_id:
            return Group(Client.get("groups/{0}".format(group_id)))

        return (Group(g) for g
                in Client.get("groups/lookup?name={0}".format(name)))
