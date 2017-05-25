from functools import total_ordering

from swimlane.core.resources.base import APIResource


@total_ordering
class UserGroup(APIResource):
    """Base class for Users and Groups
    
    Returned in some places where determining whether object is a User or Group is not possible
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
        """Converts UserGroup to raw UserGroupSelection for populating record"""
        return {
            '$type': 'Core.Models.Utilities.UserGroupSelection, Core',
            'id': self.id,
            'name': self.name
        }


class Group(UserGroup):
    """A class for working with Swimlane groups"""

    _type = 'Core.Models.Groups.Group, Core'

    def __init__(self, swimlane, raw):
        super(Group, self).__init__(swimlane, raw)

        self.description = self._raw.get('description')


class User(UserGroup):
    """Encapsulates a single Swimlane user record"""

    _type = 'Core.Models.Identity.ApplicationUser, Core'

    def __init__(self, swimlane, raw):
        super(User, self).__init__(swimlane, raw)

        self.username = self._raw.get('userName')
        self.display_name = self._raw.get('displayName')
        self.email = self._raw.get('email')
