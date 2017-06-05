from functools import total_ordering

from swimlane.core.resources.base import APIResource


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
        return isinstance(other, UserGroup) and hash(self) == hash(other)

    def __lt__(self, other):
        if not isinstance(other, UserGroup):
            raise TypeError("Comparisons not supported between instances of '{}' and '{}'".format(
                other.__class__.__name__,
                self.__class__.__name__
            ))

        return self.name < other.name

    def get_usergroup_selection(self):
        """Converts UserGroup to raw UserGroupSelection for populating record

        Returns:
            dict: Formatted UserGroup data as used by some fields
        """
        return {
            '$type': 'Core.Models.Utilities.UserGroupSelection, Core',
            'id': self.id,
            'name': self.name
        }


class Group(UserGroup):
    """A class for working with Swimlane groups

    Attributes:
        description (str): Group description
    """

    _type = 'Core.Models.Groups.Group, Core'

    def __init__(self, swimlane, raw):
        super(Group, self).__init__(swimlane, raw)

        self.description = self._raw.get('description')


class User(UserGroup):
    """Encapsulates a single Swimlane user record

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
