import mock
import unittest

from swimlane.core.resources import App
from swimlane.utils import copy_field_values


class CopyFieldValuesTestCase(unittest.TestCase):
    def setUp(self):
        self.src_app = App({
            'id': '123',
            'name': 'Source',
            'acronym': 'SO',
            'fields': [{
                'name': 'Component',
                'values': [
                    {'name': 'Foo'},
                    {'name': 'Bar'},
                    {'name': 'Baz'}],
                'fieldType': 'valuesList'}]
        })
        self.dest_app = App({
            'id': '456',
            'name': 'Destination',
            'acronym': 'DE',
            'fields': [{
                'name': 'Component',
                'values': [
                    {'name': 'Baz'},
                    {'name': 'Bar'}],
                'fieldType': 'valuesList'}]
        })

    def test_copy_field_values(self):
        with mock.patch('swimlane.core.resources.App.save') as mock_save:
            added, moved = copy_field_values(
                self.src_app, 'Component',
                self.dest_app, 'Component')
        self.assertEqual(len(added), 1)
        self.assertEqual(added[0]['name'], 'Foo')
        self.assertEqual(len(moved), 1)
        self.assertEqual(moved[0]['name'], 'Bar')
        mock_save.assert_called_once()
