import numbers
import warnings

import mock
import pytest
import six

from swimlane.core.bulk import Clear, Replace
from swimlane.exceptions import UnknownField
from swimlane.core.adapters.record import validate_filters_or_records


def test_get(mock_swimlane, mock_app, mock_record):
    mock_response = mock.MagicMock()
    mock_response.json.return_value = mock_record._raw

    with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
        assert mock_app.records.get(id='record_id') == mock_record


def test_get_by_tracking_id(mock_swimlane, mock_app, mock_record):
    mock_response = mock.MagicMock()
    # tracking_id = mock_record.tracking_id
    mock_response.json.return_value = mock_record._raw

    with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
        assert mock_app.records.get(tracking_id='record_tracking_id') == mock_record


@pytest.mark.parametrize('kwargs', [
    {'unknown_arg': 'arg'},
    {}
])
def test_invalid_args(mock_app, kwargs):
    with pytest.raises(TypeError):
        mock_app.records.get(**kwargs)


def test_create(mock_swimlane, mock_app, mock_record):
    mock_response = mock.MagicMock()
    mock_response.json.return_value = mock_record._raw

    primitives = six.string_types + (
        numbers.Number,
        list,
        tuple,
        set
    )

    fields = {}
    for field_name, field in six.iteritems(mock_record._fields):
        field_value = field.get_python()
        if isinstance(field_value, primitives) and not field.readonly:
            fields[field_name] = field_value

    with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
        assert mock_app.records.create(**fields) == mock_record


@pytest.mark.parametrize('records,expected', [
    ([], TypeError),
    ([123], TypeError),
    ([{'Nonexistent': 'Value'}], UnknownField),
    ([{}], None),
    ([{'Status': 'Open'}], None),
    ([{'Status': 'Open'}, {'Status': 'Open'}], None)
])
def test_bulk_create(mock_app, records, expected):
    if expected is not None:
        with pytest.raises(expected):
            mock_app.records.bulk_create(*records)

    else:
        mock_app.records.bulk_create(*records)


def test_search(mock_swimlane, mock_app, mock_record):
    # Run first to cache swimlane user
    with mock.patch.object(mock_swimlane._session, 'request') as mock_request:
        mock_response = mock.MagicMock()
        mock_response.json.return_value = [{
            '$type': 'Core.Models.Identity.ApplicationUser, Core',
            'active': False,
            'createdByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core'},
            'createdDate': '2017-03-31T09:10:52.717Z',
            'disabled': False,
            'displayName': 'admin',
            'groups': [],
            'id': '58de1d1c07637a0264c0ca6a',
            'isAdmin': True,
            'isMe': False,
            'lastLogin': '2017-04-27T14:11:38.54Z',
            'lastPasswordChangedDate': '2017-03-31T09:10:52.536Z',
            'modifiedByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core'},
            'modifiedDate': '2017-03-31T09:10:52.76Z',
            'name': 'admin',
            'passwordComplexityScore': 3,
            'passwordHash': 'AQAAAAEAACcQAAAAEESp9LR0jN3qPF2fw5qWdyceYxbeBbawMW5AFt31dA5n3xX16MFJWsU/j82heenFww==',
            'passwordResetRequired': False,
            'roles': [],
            'userName': 'admin'}]

        mock_request.return_value = mock_response

        # Access property to ensure call
        user = mock_swimlane.user

    mock_response = mock.MagicMock()
    mock_response.json.return_value = {
        '$type': 'API.Models.Search.GroupedSearchResults, API',
        'count': 1,
        'limit': 50,
        'offset': 0,
        'results': {
            '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[Core.Models.Record.Record[], Core]], mscorlib',
            '58e4bb4407637a0e4c4f9873': [mock_record._raw]}}

    with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
        with mock.patch('swimlane.core.adapters.report.Report._parse_raw_element', return_value=mock_record):
            assert mock_app.records.search(('Tracking Id', 'equals', 'RA-7')) == [mock_record]


def test_bulk_delete(mock_swimlane, mock_app, mock_record):
    # test that requests is called with proper object for filters
    with mock.patch.object(mock_swimlane, 'request') as mock_func:
        mock_app.records.bulk_delete(('Numeric', 'equals', 1))
    mock_func.assert_called_once_with('DELETE', "app/{0}/record/batch".format(mock_app.id), json=
    {
        'filters': [{
            'fieldId': 'aqkg3', 'filterType': 'equals', 'value': 1
        }],
    })

    # test that requests is called with proper object for records
    with mock.patch.object(mock_swimlane, 'request') as mock_func:
        mock_app.records.bulk_delete(mock_record)
    mock_func.assert_called_once_with('DELETE', "app/{0}/record/batch".format(mock_app.id), json=
    {
        'recordIds': ['58ebb22807637a02d4a14bd6']
    })

    # test value error
    with pytest.raises(ValueError):
        mock_app.records.bulk_delete(mock_record, ('Numeric', 'equals', 1))


def test_filters_or_records_validation(mock_record):
    # No values provided should raise ValueError
    with pytest.raises(ValueError):
        validate_filters_or_records([])

    # Invalid type should raise ValueError
    with pytest.raises(ValueError):
        validate_filters_or_records(["not supported type"])
    #
    with pytest.raises(ValueError):
        validate_filters_or_records([mock_record, ('Number', 'equals', 1)])


def test_bulk_modify_by_filter(mock_swimlane, mock_app):
    """Test bulk modify by filter tuples updates records"""
    # patch swimlane.requests method to assert_called_once_with
    with mock.patch.object(mock_swimlane, 'request') as mock_func:
        mock_app.records.bulk_modify(('Numeric', 'equals', 1), values={'Numeric': 2})
    mock_func.assert_called_once_with('put', "app/{0}/record/batch".format(mock_app.id), json=
    {'filters': [{
        'fieldId': 'aqkg3', 'filterType': 'equals', 'value': 1
    }],
        'modifications': [{
            'fieldId': {
                'type': 'id',
                'value': 'aqkg3'
            },
            'type': 'create', 'value': 2
        }]
    }
                                      )


def test_bulk_modify_by_record(mock_swimlane, mock_app, mock_record):
    """Test bulk modify by record/list of records"""
    # patch swimlane.requests method to assert_called_once_with
    with mock.patch.object(mock_swimlane, 'request') as mock_func:
        mock_app.records.bulk_modify(mock_record, values={'Numeric': 2})
    mock_func.assert_called_once_with('put', "app/{0}/record/batch".format(mock_app.id), json=
    {'modifications': [{
        'fieldId': {
            'type': 'id', 'value': 'aqkg3'
        },
        'type': 'create', 'value': 2
    }],
        'recordIds': ['58ebb22807637a02d4a14bd6']
    }
                                      )
    # Ensure record field is being set
    assert mock_record['Numeric'] == 2


def test_bulk_modify_errors(mock_app, mock_record):
    """Test bulk modify for expected ValueError on invalid inputs"""
    # ValueError when passing in combination of filter tuples and records
    with pytest.raises(ValueError):
        mock_app.records.bulk_modify(mock_record, ('Numeric', 'equals', 1), values={'Numeric': 2})
    # ValueError when values kwarg is missing
    with pytest.raises(ValueError):
        mock_app.records.bulk_modify(mock_record, 2)
    # ValueError when values is not dict
    with pytest.raises(ValueError):
        mock_app.records.bulk_modify(mock_record, values=2)
    # ValueError when additional kwargs beyond values
    with pytest.raises(ValueError):
        mock_app.records.bulk_modify(mock_record, values={}, other_val={})
    # ValueError when using unsupported fields
    with pytest.raises(ValueError):
        mock_app.records.bulk_modify(mock_record, values={'PCAP Attachment': mock_record['PCAP Attachment']})


def test_bulk_format_patch(mock_record, mock_group, mock_user):
    # test if case multiselect (Values List)
    value_field = mock_record.get_field('Values List')
    value_cursor = mock_record['Values List']
    assert len(value_cursor) == 2
    assert value_field.get_bulk_modify(value_cursor) != value_field.get_report(value_cursor)

    # test if case singleselect (Values List)

    mock_record['Status'] = 'Closed'
    single_value_field = mock_record.get_field('Status')
    assert single_value_field.get_bulk_modify('Closed') != single_value_field.get_report('Closed')

    # test else case multiselect (User/Groups)

    group_value = mock_record['User/Groups']
    group_field = mock_record.get_field('User/Groups')
    mock_record['User/Groups'] = [mock_group, mock_user]
    assert len(group_value) == 2
    assert group_field.get_bulk_modify(group_value) == group_field.get_report(group_value)

    # test else case singleselect

    single_group_field = mock_record._fields['User/Groups']
    single_group_field.set_swimlane([{'$type': 'Core.Models.Utilities.UserGroupSelection, Core'}])
    single_group_value = mock_record['User/Groups']
    assert single_group_field.get_bulk_modify(single_group_value) == single_group_field.get_report(single_group_value)


def test_bulk_modify_operations(mock_swimlane, mock_app, mock_record):
    """Test that the various bulk modification operators can be used as bulk_modify values"""
    with mock.patch.object(mock_swimlane, 'request') as mock_func:
        mock_app.records.bulk_modify(
            mock_record,
            values={
                'Numeric': Clear()
            }
        )

    mock_func.assert_called_once_with('put', "app/{0}/record/batch".format(mock_app.id), json={
        'modifications': [{
            'fieldId': {
                'type': 'id',
                'value': 'aqkg3'
            },
            'type': 'delete',
            'value': None
        }],
        'recordIds': ['58ebb22807637a02d4a14bd6']
    })

    with mock.patch.object(mock_swimlane, 'request') as mock_func:
        mock_app.records.bulk_modify(
            mock_record,
            values={
                'Numeric': Replace(3)
            }
        )

    mock_func.assert_called_once_with('put', "app/{0}/record/batch".format(mock_app.id), json={
        'modifications': [{
            'fieldId': {
                'type': 'id',
                'value': 'aqkg3'
            },
            'type': 'create',
            'value': 3
        }],
        'recordIds': ['58ebb22807637a02d4a14bd6']
    })
