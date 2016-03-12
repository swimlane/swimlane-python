import mock
import unittest

from swimlane.core.resources import StatsReport


MOCK_STATS_REPORT = {
    'id': '123',
    'name': 'Mock Stats Report'
}


class StatsReportTestCase(unittest.TestCase):
    def test_init(self):
        stats_report = StatsReport(MOCK_STATS_REPORT)
        for key, value in MOCK_STATS_REPORT.items():
            self.assertEqual(getattr(stats_report, key), value)

    def test_new_for(self):
        stats_report = StatsReport.new_for('123', '456', 'Test Report')
        self.assertIsInstance(stats_report, StatsReport)

    @mock.patch('swimlane.core.resources.report.Client', autospec=True)
    def test_find_all(self, mock_client):
        StatsReport.find_all()
        mock_client.get.assert_called_with('reports/all')
        StatsReport.find_all('123')
        mock_client.get.assert_called_with('reports/all?appId=123')
