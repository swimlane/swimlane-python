from swimlane.core.resources.base import APIResource, SwimlaneResolver


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

    def __eq__(self, other):
        return isinstance(other, UserGroup) and hash(self) == hash(other)

    def __hash__(self):
        return hash((self.id, self.name))

    def get_usergroup_selection(self):
        """Converts UserGroup to raw UserGroupSelection for populating record"""
        return {
            '$type': 'Core.Models.Utilities.UserGroupSelection, Core',
            'id': self.id,
            'name': self.name
        }

    @classmethod
    def from_usergroup_selection(cls, swimlane, raw):
        """Returns UserGroup instance from UserGroupSelection data as best available representation"""
        # Ultimately a pass-through to default instantiation until a differentiation is provided between Users and
        # Groups in the raw UserGroupSelection data
        return UserGroup(swimlane, raw)


class GroupAdapter(SwimlaneResolver):

    def list(self):
        response = self._swimlane.request('get', 'groups')
        return [Group(self._swimlane, raw_group_data) for raw_group_data in response.json().get('groups', [])]

    def get(self, **kwargs):
        """Retrieve single group record by id or name"""
        group_id = kwargs.pop('id', None)
        name = kwargs.pop('name', None)

        if kwargs:
            raise TypeError('Unexpected arguments: {}'.format(kwargs))

        if group_id is None and name is None:
            raise TypeError('Must provide either id or name argument')

        if group_id and name:
            raise TypeError('Cannot provide both id and name arguments')

        if group_id:
            response = self._swimlane.request('get', 'groups/{}'.format(group_id))
            return Group(self._swimlane, response.json())

        else:
            response = self._swimlane.request('get', 'groups/lookup?name={}'.format(name))
            matched_groups = response.json()

            for group_data in matched_groups:
                if group_data.get('name') == name:
                    return Group(self._swimlane, group_data)
            else:
                raise ValueError('Unable to find group with name "{}"'.format(name))


class Group(UserGroup):
    """A class for working with Swimlane groups"""

    _type = 'Core.Models.Groups.Group, Core'

    def __init__(self, swimlane, raw):
        super(Group, self).__init__(swimlane, raw)

        self.description = self._raw.get('description')


class UserAdapter(SwimlaneResolver):

    def list(self):
        """Retrieve all users"""
        response = self._swimlane.request('get', "user")
        return [User(self._swimlane, raw_user_data) for raw_user_data in response.json().get('users', [])]

    def get(self, **kwargs):
        """Retrieve single user record by id or username"""
        user_id = kwargs.pop('id', None)
        username = kwargs.pop('username', None)

        if kwargs:
            raise TypeError('Unexpected arguments: {}'.format(kwargs))

        if user_id is None and username is None:
            raise TypeError('Must provide either id or username argument')

        if user_id and username:
            raise TypeError('Cannot provide both id and username arguments')

        if user_id:
            response = self._swimlane.request('get', 'user/{}'.format(user_id))
            return User(self._swimlane, response.json())

        else:
            response = self._swimlane.request('get', 'user/search?query={}'.format(username))
            matched_users = response.json()

            for user_data in matched_users:
                if user_data.get('userName') == username:
                    return User(self._swimlane, user_data)
            else:
                raise ValueError('Unable to find user with username "{}"'.format(username))


class User(UserGroup):
    """Encapsulates a single Swimlane user record"""

    _type = 'Core.Models.Identity.ApplicationUser, Core'

    def __init__(self, swimlane, raw):
        super(User, self).__init__(swimlane, raw)

        self.username = self._raw.get('userName')
        self.display_name = self._raw.get('displayName')
