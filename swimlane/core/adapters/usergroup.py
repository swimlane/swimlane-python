from six.moves.urllib.parse import quote_plus

from swimlane.core.resolver import SwimlaneResolver
from swimlane.core.resources import Group, User


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

            raise ValueError('Unable to find group with name "{}"'.format(name))


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
            # TODO: Investigate users with special characters not being returned
            response = self._swimlane.request('get', 'user/search?query={}'.format(quote_plus(username)))
            matched_users = response.json()

            for user_data in matched_users:
                if user_data.get('userName') == username:
                    return User(self._swimlane, user_data)

            raise ValueError('Unable to find user with username "{}"'.format(username))
