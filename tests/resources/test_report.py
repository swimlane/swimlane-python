import mock
import pytest

from swimlane.exceptions import UnknownField


class TestReport(object):

    def test_repr(self, mock_report):
        assert repr(mock_report) == '<Report: search-12345678>'

    def test_filter(self, mock_report):
        """Test adding a filter to a report"""

        # Attempt to use an operand the reports don't understand
        with pytest.raises(ValueError):
            mock_report.filter('Tracking Id', 'Invalid Operand', 'RA-7')

        # Attempt to filter on an invalid field
        with pytest.raises(UnknownField):
            mock_report.filter('TrackingId', "equals", 'RA-7')

        assert len(mock_report._raw['filters']) == 0
        mock_report.filter('Tracking Id', 'equals', 'RA-7')

        assert len(mock_report._raw['filters']) == 1

    def test_iteration(self, mock_report, mock_record, mock_swimlane):
        """Test iterating over report results"""
        with mock.patch.object(mock_swimlane, 'request') as mock_request:
            mock_response = mock.MagicMock()
            mock_request.return_value = mock_response

            mock_response.json.return_value = {
                '$type': 'API.Models.Search.GroupedSearchResults, API',
                'count': 1,
                'limit': 50,
                'offset': 0,
                'results': {
                    '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[Core.Models.Record.Record[], Core]], mscorlib',
                    '58e4bb4407637a0e4c4f9873': [mock_record._raw]}}

            assert mock_request.call_count == 0

            results = list(mock_report)

            assert len(results) == 1
            assert results[0] == mock_record

            assert mock_request.call_count == 1

            # Run again to check cache records returned instead of making additional requests
            results = list(mock_report)
            assert len(results) == 1
            assert mock_request.call_count == 1


