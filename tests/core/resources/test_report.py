import mock
import unittest

from swimlane.core.resources import Report
from swimlane.core.search.filtering import create_filter, EQ
MOCK_REPORT = {
    'id': '123',
    'name': 'Mock Report'
}


class ReportTestCase(unittest.TestCase):
    def test_init(self):
        report = Report(MOCK_REPORT)
        for key, value in MOCK_REPORT.items():
            self.assertEqual(getattr(report, key), value)

    @mock.patch('swimlane.core.resources.report.Client', autospec=True)
    def test_insert(self, mock_client):
        report = Report(MOCK_REPORT)
        report.insert()
        mock_client.post.assert_called_once_with(report, 'reports')

    @mock.patch('swimlane.core.resources.report.Client', autospec=True)
    def test_update(self, mock_client):
        report = Report(MOCK_REPORT)
        report.update()
        mock_client.put.assert_called_once_with(report, 'reports')

    def test_new_for(self):
        report = Report.new_for('123', '456', 'New Report')
        self.assertIsInstance(report, Report)

    @mock.patch('swimlane.core.resources.report.Client', autospec=True)
    def test_find_all(self, mock_client):
        Report.find_all()
        mock_client.get.assert_called_with('reports/all')
        Report.find_all('123')
        mock_client.get.assert_called_with('reports/all?appId=123')

    @mock.patch('swimlane.core.resources.report.Client', autospec=True)
    def test_find(self, mock_client):
        Report.find('123')
        mock_client.get.assert_called_once_with('reports/123')
