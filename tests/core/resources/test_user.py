import mock
import unittest

from swimlane.core.resources import User


MOCK_USER = {
    'id': '123',
    'name': 'Mock User'
}

MOCK_USERS = {
    'users': [MOCK_USER]
}


class UserTestCase(unittest.TestCase):
    def test_init(self):
        user = User(MOCK_USER)
        for key, value in MOCK_USER.items():
            self.assertEqual(getattr(user, key), value)

    @mock.patch('swimlane.core.resources.user.Client', autospec=True)
    def test_find_all(self, mock_client):
        mock_client.get.return_value = MOCK_USERS
        users = list(User.find_all())
        self.assertEqual(len(users), 1)
        self.assertIsInstance(users[0], User)

    @mock.patch('swimlane.core.resources.user.Client', autospec=True)
    def test_find_by_id(self, mock_client):
        mock_client.get.return_value = MOCK_USER
        user = User.find(user_id='123')
        self.assertIsInstance(user, User)
        self.assertEqual(user.id, '123')

    @mock.patch('swimlane.core.resources.user.Client', autospec=True)
    def test_find_by_name(self, mock_client):
        mock_client.get.return_value = MOCK_USERS
        users = list(User.find(name='Mock User'))
        self.assertEqual(len(users), 1)
        self.assertIsInstance(users[0], User)

    @mock.patch('swimlane.core.resources.user.Client', autospec=True)
    def test_find_by_name_does_not_exist(self, mock_client):
        mock_client.get.return_value = []
        users = User.find(name='Some Other User')
        self.assertEqual(list(users), [])
