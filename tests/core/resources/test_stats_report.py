import mock
import unittest

from swimlane.core.resources import StatsReport, User


MOCK_STATS_REPORT = {
    'id': '123',
    'name': 'Mock Stats Report'
}


MOCK_USER = User(fields={
    'id': '123',
    'name': 'Mock User'
})


class StatsReportTestCase(unittest.TestCase):
    def test_init(self):
        stats_report = StatsReport(MOCK_STATS_REPORT)
        for key, value in MOCK_STATS_REPORT.items():
            self.assertEqual(getattr(stats_report, key), value)

    @mock.patch('swimlane.core.resources.report.User', autospec=True)
    def test_new_for(self, mock_user):
        mock_user.find.return_value = MOCK_USER
        stats_report = StatsReport.new_for('123', '456', 'Test Report')
        self.assertIsInstance(stats_report, StatsReport)

    @mock.patch('swimlane.core.resources.report.Client', autospec=True)
    def test_find_all(self, mock_client):
        StatsReport.find_all()
        mock_client.get.assert_called_with('reports')
        StatsReport.find_all('123')
        mock_client.get.assert_called_with('reports?appId=123')
