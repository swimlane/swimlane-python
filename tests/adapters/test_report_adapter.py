import mock

from swimlane.core.resources.report import Report

raw_report = {'$type': 'Core.Models.Search.Report, Core',
              'aggregates': [],
              'allowed': [],
              'applicationIds': ['58de205f07637a0264c0ccbf'],
              'columns': ['58de205f07637a0264c0ccc1'],
              'createdByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                'id': '58de1d1c07637a0264c0ca6a',
                                'name': 'admin'},
              'createdDate': '2017-03-31T09:24:47.758Z',
              'defaultSearchReport': True,
              'disabled': False,
              'filters': [],
              'groupBys': [],
              'id': '58de205f07637a0264c0ccc5',
              'modifiedByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                                 'id': '58de1d1c07637a0264c0ca6a',
                                 'name': 'admin'},
              'modifiedDate': '2017-03-31T09:24:47.758Z',
              'name': 'Default',
              'offset': 0,
              'pageSize': 10,
              'permissions': {'$type': 'Core.Models.Security.PermissionMatrix, Core'},
              'sorts': {
                  '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[Core.Models.Search.SortTypes, Core]], mscorlib',
                  '58de205f07637a0264c0ccc1': 'ascending'}}


def test_list(mock_app, mock_swimlane):
    mock_response = mock.MagicMock()
    mock_response.json.return_value = [raw_report for _ in range(3)]

    with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
        reports = mock_app.reports.list()
        assert len(reports) == 3
        for report in reports:
            assert isinstance(report, Report)


def test_get(mock_app, mock_swimlane):
    mock_response = mock.MagicMock()
    mock_response.json.return_value = raw_report

    with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
        report = mock_app.reports.get(report_id='report_id')
        assert isinstance(report, Report)
