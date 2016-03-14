import mock
import unittest

from swimlane.core.resources import StatsReport
from swimlane.core.search import Search
from swimlane.core.search.search_result import SearchResult


class SearchTestCase(unittest.TestCase):
    def test_init(self):
        mock_report = mock.Mock()
        search = Search(mock_report)
        self.assertEqual(search.report, mock_report)
        self.assertFalse(search.has_more_pages)
        pass

    @mock.patch('swimlane.core.search.search.Client', autospec=True)
    def test_execute(self, mock_client):
        mock_response = {
            'count': '1',
            'limit': '1',
            'offset': '1',
            'results': []
        }
        mock_client.post.return_value = mock_response

        report = StatsReport({
            'applicationIds': [{}],
            'offset': 1,
            'pageSize': 1})
        search = Search(report)
        search_result = search.execute()

        mock_client.post.assert_called_once_with(report, 'search/stats')
        self.assertIsInstance(search_result, SearchResult)

        mock_client.post.return_value = (r for r in [mock_response])
        search.next_page()
        self.assertEqual(len(mock_client.post.mock_calls), 2)
