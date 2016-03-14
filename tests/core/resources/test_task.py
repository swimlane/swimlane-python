import mock
import unittest

from swimlane.core.resources import Task


MOCK_TASK = {
    'id': '123',
    'name': 'Mock Task'
}


class TaskTestCase(unittest.TestCase):
    def test_init(self):
        task = Task(MOCK_TASK)
        for key, value in MOCK_TASK.items():
            self.assertEqual(getattr(task, key), value)

    @mock.patch('swimlane.core.resources.task.Client', autospec=True)
    def test_run(self, mock_client):
        mock_record = mock.MagicMock()
        mock_record._fields = {'foo': 'bar'}
        task = Task(MOCK_TASK)
        task.run(mock_record)
        mock_client.post.assert_called_once_with({
            'taskId': task.id,
            'record': mock_record._fields},
            'task/execute/record')

    @mock.patch('swimlane.core.resources.task.Client', autospec=True)
    def test_find_all(self, mock_client):
        Task.find_all()
        mock_client.get.assert_called_once_with('task/light')

    @mock.patch('swimlane.core.resources.task.Client', autospec=True)
    def test_find(self, mock_client):
        Task.find('Mock Task')
        mock_client.get.assert_called_once_with('task/light')
