from .base import APIResource, APIResourceAdapter


class UserAdapter(APIResourceAdapter):

    def list(self):
        """Retrieve all users"""
        response = self.swimlane.request('get', "user")
        return [User(self.swimlane, raw_user_data) for raw_user_data in response.json().get('users', [])]

    def get(self, user_id=None, username=None):
        """Retrieve single user record"""
        if user_id is None and username is None:
            raise ValueError('Must provide either user_id or name')

        if user_id:
            response = self.swimlane.request('get', 'user/{}'.format(user_id))
            return User(self.swimlane, response.json())

        else:
            response = self.swimlane.request('get', 'user/search?query={}'.format(username))
            matched_users = response.json()

            for user_data in matched_users:
                if user_data.get('userName') == username:
                    return User(self.swimlane, user_data)
            else:
                raise ValueError('Unable to find user with username "{}"'.format(username))


class User(APIResource):
    """Encapsulates a single Swimlane user record"""

    _type = 'Core.Models.Identity.ApplicationUser, Core'

    def __init__(self, swimlane, raw):
        super(User, self).__init__(swimlane, raw)

        self.id = self._raw['id']
        self.username = self._raw['userName']
        self.display_name = self._raw['displayName']
        self.name = self._raw['name']

    def get_user_selection(self):
        """Converts User to UserSelection for populating record"""
        return {
            '$type': 'Core.Models.Utilities.UserGroupSelection, Core',
            'id': self.id,
            'name': self.name
        }
