import mock

from swimlane.core.resources import Record
from swimlane.errors import UnknownField


def test_repr(mock_record):

    assert repr(mock_record) == '<Record: RA-7>'


def test_save(mock_swimlane, mock_record):
    """Test save endpoint called with correct args"""

    with mock.patch.object(mock_swimlane, 'request') as mock_request:

        mock_record['Numeric'] = 5
        mock_record.save()

        mock_request.assert_called_once_with(
            'put',
            'app/{}/record'.format(mock_record._app.id),
            json=mock_record._raw
        )


def test_ordering(mock_record):
    record_copy = Record(mock_record._app, mock_record._raw)

    # Equality by id and app id
    assert record_copy == mock_record

    record_copy.id = '58ebb22807637a02d4a14bd7'

    assert record_copy != mock_record

    # Ordering by id and app id
    assert mock_record < record_copy


def test_unknown_field_access(mock_record):
    """Test accessing a missing field raises UnknownField"""

    # Get
    try:
        mock_record['Muneric']
    except UnknownField as error:
        assert error.field_name == 'Muneric'
        assert error.similar_field_names == ['Numeric']
        assert error.app is mock_record._app
    else:
        raise RuntimeError

    # Set
    try:
        mock_record['Muneric'] = 5
    except UnknownField as error:
        assert error.field_name == 'Muneric'
        assert error.similar_field_names == ['Numeric']
        assert error.app is mock_record._app
    else:
        raise RuntimeError


def test_iteration(mock_record):
    """Test that iterating over a record yields field names and their values like dict.items()"""
    num_fields = 0

    for field_name, field_value in mock_record:
        num_fields += 1
        assert field_value == mock_record[field_name]

    assert num_fields > 0
