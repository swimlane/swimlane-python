import unittest

from swimlane.core.resources import Resource


class ResourceTestCase(unittest.TestCase):
    def test_init(self):
        r = Resource({'foo': 1, 'bar': True, 'baz': None})

        self.assertEqual(r.foo, 1)
        self.assertTrue(r.bar)
        self.assertIsNone(r.baz)
        self.assertRaises(AttributeError, lambda: r.doesnotexist)
        r.bar = False
        self.assertFalse(r.bar)
        self.assertIn('foo', str(r))
