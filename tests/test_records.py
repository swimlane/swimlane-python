import mock
import unittest

from swimlane.records import add_references


class RecordsTestCase(unittest.TestCase):
    @mock.patch('swimlane.records.App', autospec=True)
    def test_add_references_app_not_found(self, mock_app):
        mock_app.find.return_value = None
        self.assertRaises(
            Exception,
            lambda: add_references('123', 'keywords'))
        mock_app.find.assert_called_once_with(app_id=None, name=None)

    @mock.patch('swimlane.records.App', autospec=True)
    def test_add_references_field_id_not_found(self, mock_app):
        mock_app_instance = mock.MagicMock()
        mock_app_instance.field_id.return_value = None
        mock_app.find.return_value = mock_app_instance
        self.assertRaises(
            Exception,
            lambda: add_references('123', 'keywords', field_name='foo'))
        mock_app_instance.field_id.assert_called_once_with('foo')
