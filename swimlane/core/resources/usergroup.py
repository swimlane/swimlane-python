from functools import total_ordering

from swimlane.core.cursor import Cursor
from swimlane.core.resolver import SwimlaneResolver
from swimlane.core.resources.base import APIResource


# pylint: disable=abstract-method
@total_ordering
class UserGroup(APIResource):
    """Base class for Users and Groups

    Notes:
        Returned in some places where determining whether object is a User or Group is not possible without additional
        requests. Use appropriate adapter on `swimlane` client to retrieve more specific instance using `id` as needed

        Can be compared to User or Group instances directly without ensuring the classes are the same

    Attributes:
        id (str): Full user/group ID
        name (str): User/group name
    """

    def __init__(self, swimlane, raw):
        super(UserGroup, self).__init__(swimlane, raw)

        self.id = self._raw['id']
        self.name = self._raw['name']

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash((self.id, self.name))

    def __eq__(self, other):
        """Override to allow equality comparisons across UserGroup, User, and Group instances"""
        return isinstance(other, UserGroup) and hash(self) == hash(other)

    def __lt__(self, other):
        if not isinstance(other, UserGroup):
            raise TypeError("Comparisons not supported between instances of '{}' and '{}'".format(
                other.__class__.__name__,
                self.__class__.__name__
            ))

        return self.name < other.name

    def resolve(self):
        """Retrieve and return correct User or Group instance from UserGroup

        .. versionadded:: 2.16.1

        Returns:
            User | Group: Resolved User or Group instance
        """
        # Skip resolving if not a generic instance
        if self.__class__ is not UserGroup:
            return self

        else:
            try:
                return self._swimlane.users.get(id=self.id)
            except ValueError:
                return self._swimlane.groups.get(id=self.id)

    def as_usergroup_selection(self):
        """Converts UserGroup to raw UserGroupSelection for populating record

        Returns:
            dict: Formatted UserGroup data as used by selection fields
        """
        return {
            '$type': 'Core.Models.Utilities.UserGroupSelection, Core',
            'id': self.id,
            'name': self.name
        }


class Group(UserGroup):
    """Swimlane group record

    Attributes:
        description (str): Group description
        users (GroupUsersCursor): List of users belonging to group.
    """

    _type = 'Core.Models.Groups.Group, Core'

    def __init__(self, swimlane, raw):
        super(Group, self).__init__(swimlane, raw)
        self.__user_ids = [item['id'] for item in self._raw.get('users')]
        self.description = self._raw.get('description')
        self.__users = None

    @property
    def users(self):
        """Returns a GroupUsersCursor with list of User instances for this Group

        .. versionadded:: 2.16.2
        """
        if self.__users is None:
            self.__users = GroupUsersCursor(swimlane=self._swimlane, user_ids=self.__user_ids)
        return self.__users

    def get_cache_index_keys(self):
        return {
            'id': self.id,
            'name': self.name
        }


class User(UserGroup):
    """Swimlane user record

    Attributes:
        username (str): Unique username
        display_name (str): User display name
        email (str): User email
    """

    _type = 'Core.Models.Identity.ApplicationUser, Core'

    def __init__(self, swimlane, raw):
        super(User, self).__init__(swimlane, raw)

        self.username = self._raw.get('userName')
        self.display_name = self._raw.get('displayName')
        self.email = self._raw.get('email')

    def get_cache_index_keys(self):
        return {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name
        }


class GroupUsersCursor(SwimlaneResolver, Cursor):
    """Handles retrieval for user endpoint"""

    def __init__(self, swimlane, user_ids):
        SwimlaneResolver.__init__(self, swimlane)
        Cursor.__init__(self)
        self.__user_ids = user_ids

    def _evaluate(self):
        """Lazily retrieve and build User instances from returned data"""
        if self._elements:
            for element in self._elements:
                yield element
        else:
            for user_id in self.__user_ids:
                element = self._swimlane.users.get(id=user_id)
                self._elements.append(element)
                yield element
