import mock
import unittest

from swimlane.core.resources import Group

MOCK_GROUP = {
    'id': '123',
    'name': 'Mock Group'
}

MOCK_GROUPS = {
    'groups': [MOCK_GROUP]
}


class GroupTestCase(unittest.TestCase):
    def test_init(self):
        group = Group(MOCK_GROUP)
        for key, value in MOCK_GROUP.items():
            self.assertEqual(getattr(group, key), value)

    @mock.patch('swimlane.core.resources.group.Client', autospec=True)
    def test_find_all(self, mock_client):
        mock_client.get.return_value = MOCK_GROUPS
        groups = list(Group.find_all())
        self.assertEqual(len(groups), 1)
        self.assertIsInstance(groups[0], Group)

    @mock.patch('swimlane.core.resources.group.Client', autospec=True)
    def test_find_by_id(self, mock_client):
        mock_client.get.return_value = MOCK_GROUP
        group = Group.find(group_id='123')
        self.assertIsInstance(group, Group)
        self.assertEqual(group.id, '123')

    @mock.patch('swimlane.core.resources.group.Client', autospec=True)
    def test_find_by_name(self, mock_client):
        mock_client.get.return_value = MOCK_GROUPS
        groups = list(Group.find(name='Mock Group'))
        self.assertEqual(len(groups), 1)
        self.assertIsInstance(groups[0], Group)

    @mock.patch('swimlane.core.resources.group.Client', autospec=True)
    def test_find_by_name_does_not_exist(self, mock_client):
        mock_client.get.return_value = []
        groups = Group.find(name='Some Other Group')
        self.assertEqual(list(groups), [])
