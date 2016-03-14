import unittest

from swimlane.core.resources import StatsResult


MOCK_STATS_RESULT = {
    'foo': 'bar'
}


class StatsResultTestCase(unittest.TestCase):
    def test_init(self):
        stats_result = StatsResult(MOCK_STATS_RESULT)
        for key, value in MOCK_STATS_RESULT.items():
            self.assertEqual(getattr(stats_result, key), value)
