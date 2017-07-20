import mock
import pytest

from swimlane.core.resources.report import report_factory
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

    def test_parse_raw_element(self, mock_app, mock_record):
        """Test _build_record makes a retrieval to the full record"""
        with mock.patch.object(mock_app.records, 'get', return_value=mock_record):
            report = report_factory(mock_app, 'build_record')
            assert report._parse_raw_element(mock_record._raw) is mock_record

    def test_limit(self, mock_record, mock_app, mock_swimlane):
        with mock.patch.object(mock_swimlane, 'request') as mock_request:
            mock_response = mock.MagicMock()
            mock_request.return_value = mock_response

            mock_response.json.return_value = {
                '$type': 'API.Models.Search.GroupedSearchResults, API',
                'count': 2,
                'limit': 50,
                'offset': 0,
                'results': {
                    '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[Core.Models.Record.Record[], Core]], mscorlib',
                    '58e4bb4407637a0e4c4f9873': [mock_record._raw for i in range(50)]}}

            with mock.patch('swimlane.core.resources.report.Report._parse_raw_element', return_value=mock_record):
                report = report_factory(mock_app, 'limit_test', limit=5)
                assert len(report) == 5

                report = report_factory(mock_app, 'default_limit')
                assert len(report) == 50

                report = report_factory(mock_app, 'no_limit', limit=100)
                assert len(report) == 100

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
            with mock.patch.object(mock_report, '_parse_raw_element', return_value=mock_record):

                results = list(mock_report)

                assert len(results) == 1
                assert results[0] == mock_record

                assert mock_request.call_count == 1

                # Run again to check cache records returned instead of making additional requests
                results = list(mock_report)
                assert len(results) == 1
                assert mock_request.call_count == 1


