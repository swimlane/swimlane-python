from six.moves.urllib.parse import quote_plus

from swimlane.core.resolver import SwimlaneResolver
from swimlane.core.resources import Group, User


class GroupAdapter(SwimlaneResolver):
    """Handles retrieval of Swimlane Group resources"""

    def list(self):
        """Retrieve list of all groups

        Returns:
            :obj:`list` of :obj:`Group`: List of all Groups
        """
        response = self._swimlane.request('get', 'groups')
        return [Group(self._swimlane, raw_group_data) for raw_group_data in response.json().get('groups', [])]

    def get(self, **kwargs):
        """Retrieve single group record by id or name

        Keyword Args:
            id (str): Full Group ID
            name (str): Group name

        Raises:
            TypeError: Unexpected or more than one keyword argument provided
            ValueError: No matching group found based on provided inputs

        Returns:
            Group: Group instance matching provided inputs
        """
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
    """Handles retrieval of Swimlane User resources"""

    def list(self):
        """Retrieve all users

        Returns:
            :obj:`list` of :obj:`User`: List of all Users
        """
        response = self._swimlane.request('get', "user")
        return [User(self._swimlane, raw_user_data) for raw_user_data in response.json().get('users', [])]

    def get(self, **kwargs):
        """Retrieve single user record by id or username

        Notes:
            If using `display_name`, method will fail if multiple Users are returned with the same display name

        Keyword Args:
            id (str): Full User ID
            display_name (str): User display name

        Returns:
            User: User instance matching provided inputs

        Raises:
            TypeError: Unexpected or more than one keyword argument provided
            ValueError: No matching user found based on provided inputs, or multiple Users with same display name
        """
        user_id = kwargs.pop('id', None)
        display_name = kwargs.pop('display_name', None)

        if kwargs:
            raise TypeError('Unexpected arguments: {}'.format(kwargs))

        if user_id is None and display_name is None:
            raise TypeError('Must provide either id or display_name argument')

        if user_id and display_name:
            raise TypeError('Cannot provide both id and display_name arguments')

        if user_id:
            response = self._swimlane.request('get', 'user/{}'.format(user_id))
            return User(self._swimlane, response.json())

        else:
            response = self._swimlane.request('get', 'user/search?query={}'.format(quote_plus(display_name)))
            matched_users = response.json()

            # Display name not unique, fail if multiple users share the same target display name
            target_matches = []

            for user_data in matched_users:
                user_display_name = user_data.get('displayName')
                if user_display_name == display_name:
                    target_matches.append(user_data)

            # No matches
            if not target_matches:
                raise ValueError('Unable to find user with display name "{}"'.format(display_name))

            # Multiple matches
            if len(target_matches) > 1:
                raise ValueError('Multiple users returned with display name "{}". Matching user IDs: {}'.format(
                    display_name,
                    ', '.join(['"{}"'.format(r['id']) for r in target_matches])
                ))

            return User(self._swimlane, target_matches[0])
