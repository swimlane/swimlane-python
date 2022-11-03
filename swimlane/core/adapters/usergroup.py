from six.moves.urllib.parse import quote_plus

from swimlane.core.cache import check_cache
from swimlane.core.cursor import PaginatedCursor
from swimlane.core.resolver import SwimlaneResolver
from swimlane.core.resources.usergroup import Group, User
from swimlane.utils import one_of_keyword_only
from typing import Optional, Any, List


class GroupListCursor(SwimlaneResolver, PaginatedCursor):
    """Handles retrieval and pagination of group list endpoint"""

    def __init__(self, swimlane: Any, limit: Optional[int]=None) -> None:
        SwimlaneResolver.__init__(self, swimlane)
        PaginatedCursor.__init__(self, limit)

    def _parse_raw_element(self, raw_element: Any) -> Group:
        return Group(self._swimlane, raw_element)

    def _retrieve_raw_elements(self, page: int) -> List[Any]:
        response = self._swimlane.request(
            'get',
            'groups',
            params={
                'size': self.page_size,
                'pageNumber': page
            }
        )
        return response.json().get('items', [])


class GroupAdapter(SwimlaneResolver):
    """Handles retrieval of Swimlane Group resources"""

    def list(self, limit: Optional[int] = None) -> GroupListCursor:
        """Retrieve list of all groups

        Returns:
            :class:`list` of :class:`~swimlane.core.resources.usergroup.Group`: List of all Groups
        """
        return GroupListCursor(self._swimlane, limit=limit)

    @check_cache(Group)
    @one_of_keyword_only('id', 'name')
    def get(self, key: str, value: str) -> Group:
        """Retrieve single group record by id or name

        Supports resource cache

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


class UserListCursor(SwimlaneResolver, PaginatedCursor):
    """Handles retrieval and pagination for user list endpoint"""

    def __init__(self, swimlane: Any, limit: Optional[int] = None) -> None:
        SwimlaneResolver.__init__(self, swimlane)
        PaginatedCursor.__init__(self, limit)

    def _parse_raw_element(self, raw_element: Any) -> User:
        return User(self._swimlane, raw_element)

    def _retrieve_raw_elements(self, page: int) -> Any:
        response = self._swimlane.request(
            'get',
            'user',
            params={
                'size': self.page_size,
                'pageNumber': page
            }
        )
        return response.json().get('items', [])


class UserAdapter(SwimlaneResolver):
    """Handles retrieval of Swimlane User resources"""

    def list(self, limit: Optional[int] = None) -> UserListCursor:
        """Retrieve all users

        Returns:
            :class:`UserListCursor`: Paginated cursor yielding :class:`User` instances
        """
        return UserListCursor(swimlane=self._swimlane, limit=limit)

    @check_cache(User)
    @one_of_keyword_only('id', 'display_name')
    def get(self, arg: str, value: str) -> User:
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
