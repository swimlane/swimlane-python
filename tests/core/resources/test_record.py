import mock
import unittest

from swimlane.core.resources import Record


MOCK_RECORD = {
    'id': '123',
    'applicationId': '456',
    'values': {
        'foo': 'bar'
    }
}


class RecordTestCase(unittest.TestCase):
    def test_init(self):
        record = Record(MOCK_RECORD)
        for key, value in MOCK_RECORD.items():
            self.assertEqual(getattr(record, key), value)

    @mock.patch('swimlane.core.resources.record.Client', autospec=True)
    def test_insert(self, mock_client):
        mock_client.post.return_value = MOCK_RECORD
        record = Record(MOCK_RECORD)
        record.insert()
        mock_client.post.assert_called_once_with(record, 'app/456/record')

    @mock.patch('swimlane.core.resources.record.Client', autospec=True)
    def test_update(self, mock_client):
        mock_client.put.return_value = MOCK_RECORD
        record = Record(MOCK_RECORD)
        record.isNew = False
        record.update()
        mock_client.put.assert_called_once_with(record, 'app/456/record')

    @mock.patch('swimlane.core.resources.record.Client', autospec=True)
    def test_add_comment(self, mock_client):
        record = Record(MOCK_RECORD)
        record.add_comment('123', '456', 'Test Comment')
        mock_client.post.assert_called_once_with({
            'message': 'Test Comment',
            'createdDate': mock.ANY,
            'createdByUser': '456'
        }, 'app/456/record/123/123/comment')

    @mock.patch('swimlane.core.resources.record.Client', autospec=True)
    def test_references(self, mock_client):
        record = Record(MOCK_RECORD)
        record.references('123', ['456'], ['789'])
        mock_client.get.assert_called_once_with(
            'app/456/record/123/references?recordIds=456&fieldIds=789')

    @mock.patch('swimlane.core.resources.record.Client', autospec=True)
    def test_new_for(self, mock_client):
        Record.new_for('123')
        mock_client.get.assert_called_once_with(
            'app/123/record')

    @mock.patch('swimlane.core.resources.record.Client', autospec=True)
    def test_find(self, mock_client):
        Record.find('123', '456')
        mock_client.get.assert_called_once_with('app/123/record/456')
