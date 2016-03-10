import unittest

from swimlane.core import SwimlaneDict


D = {
    'one': 1,
    'two': 2,
    'values': {
        'four': 4,
        'five': 5,
        '$type': 'GARBAGE',
        'six': {
            'seven': 7,
            '$type': 'MOREGARBAGE',
            'eight': 8,
            'nine': {
                'ten': 10,
                '$type': 'EVENMOREGARBAGE'
            }
        }
    },
    '$type': 'TOPLEVELGARBAGE'
}


class SwimlaneDictTestCase(unittest.TestCase):
    def test_swimlane_dict(self):
        sd = SwimlaneDict(D)
        self.assertEqual(('$type', 'TOPLEVELGARBAGE'), sd.popitem(last=False))
        self.assertEqual(
            ('$type', 'GARBAGE'),
            sd['values'].popitem(last=False))
        self.assertEqual(
            ('$type', 'MOREGARBAGE'),
            sd['values']['six'].popitem(last=False))
        self.assertEqual(
            ('$type', 'EVENMOREGARBAGE'),
            sd['values']['six']['nine'].popitem(last=False))
