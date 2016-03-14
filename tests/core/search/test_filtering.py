import unittest

from swimlane.core.search.filtering import create_filter

class FilteringTestCase(unittest.TestCase):
    def test_create_filter(self):
        filter = create_filter('foo', 'equals', 'bar')
        self.assertEqual(filter, {
            'fieldId': 'foo',
            'filterType': 'equals',
            'value': 'bar'})
