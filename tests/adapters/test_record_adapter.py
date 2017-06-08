import numbers

import mock
import pytest
import six

from swimlane.exceptions import UnknownField


def test_get(mock_swimlane, mock_app, mock_record):
    mock_response = mock.MagicMock()
    mock_response.json.return_value = mock_record._raw

    with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
        assert mock_app.records.get(id='record_id') == mock_record


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
def test_create_batch(mock_app, records, expected):
    if expected is not None:
        with pytest.raises(expected):
            mock_app.records.create_batch(*records)

    else:
        mock_app.records.create_batch(*records)


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
        assert mock_app.records.search(('Tracking Id', 'equals', 'RA-7')) == [mock_record]
