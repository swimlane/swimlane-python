from six.moves.urllib.parse import quote_plus

from swimlane.core.resolver import SwimlaneResolver
from swimlane.core.resources import Group, User
from swimlane.utils import one_of_keyword_only


class GroupAdapter(SwimlaneResolver):
    """Handles retrieval of Swimlane Group resources"""

    def list(self):
        """Retrieve list of all groups

        Returns:
            :class:`list` of :class:`~swimlane.core.resources.usergroup.Group`: List of all Groups
        """
        response = self._swimlane.request('get', 'groups')
        return [Group(self._swimlane, raw_group_data) for raw_group_data in response.json().get('groups', [])]

    @one_of_keyword_only('id', 'name')
    def get(self, key, value):
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
        if key == 'id':
            response = self._swimlane.request('get', 'groups/{}'.format(value))
            return Group(self._swimlane, response.json())

        else:
            response = self._swimlane.request('get', 'groups/lookup?name={}'.format(value))
            matched_groups = response.json()

            for group_data in matched_groups:
                if group_data.get('name') == value:
                    return Group(self._swimlane, group_data)

            raise ValueError('Unable to find group with name "{}"'.format(value))


class UserAdapter(SwimlaneResolver):
    """Handles retrieval of Swimlane User resources"""

    def list(self):
        """Retrieve all users

        Returns:
            :class:`list` of :class:`~swimlane.core.resources.usergroup.User`: List of all Users
        """
        response = self._swimlane.request('get', "user")
        return [User(self._swimlane, raw_user_data) for raw_user_data in response.json().get('users', [])]

    @one_of_keyword_only('id', 'display_name')
    def get(self, arg, value):
        """Retrieve single user record by id or username

        Warnings:
            User display names are not unique. If using `display_name`, method will fail if multiple Users are returned
            with the same display name

        Keyword Args:
            id (str): Full User ID
            display_name (str): User display name

        Returns:
            User: User instance matching provided inputs

        Raises:
            TypeError: Unexpected or more than one keyword argument provided
            ValueError: No matching user found based on provided inputs, or multiple Users with same display name
        """
        if arg == 'id':
            response = self._swimlane.request('get', 'user/{}'.format(value))

            try:
                user_data = response.json()
            except ValueError:
                raise ValueError('Unable to find user with ID "{}"'.format(value))

            return User(self._swimlane, user_data)

        else:
            response = self._swimlane.request('get', 'user/search?query={}'.format(quote_plus(value)))
            matched_users = response.json()

            # Display name not unique, fail if multiple users share the same target display name
            target_matches = []

            for user_data in matched_users:
                user_display_name = user_data.get('displayName')
                if user_display_name == value:
                    target_matches.append(user_data)

            # No matches
            if not target_matches:
                raise ValueError('Unable to find user with display name "{}"'.format(value))

            # Multiple matches
            if len(target_matches) > 1:
                raise ValueError('Multiple users returned with display name "{}". Matching user IDs: {}'.format(
                    value,
                    ', '.join(['"{}"'.format(r['id']) for r in target_matches])
                ))

            return User(self._swimlane, target_matches[0])
