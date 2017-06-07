import mock
import pytest

from swimlane.core.resources.record import Record, record_factory
from swimlane.exceptions import UnknownField, ValidationError


class TestRecord(object):
    def test_repr(self, mock_record):
        assert repr(mock_record) == '<Record: RA-7>'
        assert repr(record_factory(mock_record._app)) == '<Record: RA - New>'

    def test_save(self, mock_swimlane, mock_record):
        """Test save endpoint called with correct args"""

        with mock.patch.object(mock_swimlane, 'request') as mock_request:
            with mock.patch.object(mock_record, 'validate') as mock_validate:

                mock_request.return_value.json.return_value = mock_record._raw

                mock_record['Numeric'] = 5
                mock_record.save()

                mock_validate.assert_called_once_with()
                mock_request.assert_called_once_with(
                    'put',
                    'app/{}/record'.format(mock_record._app.id),
                    json=mock_record._raw
                )

                # Test validation failure
                mock_validate.side_effect = ValidationError(mock_record, 'Test error')

                with pytest.raises(ValidationError):
                    mock_record.save()

                assert mock_validate.call_count == 2
                assert mock_request.call_count == 1

    def test_validate_required_fields(self, mock_record):
        """Test validate method checks for required fields"""
        assert mock_record.validate() is None

        field_name = 'Numeric'
        mock_record[field_name] = None
        mock_record._fields[field_name].required = True

        with pytest.raises(ValidationError):
            mock_record.validate()

    def test_ordering(self, mock_record, mock_app):
        record_copy = Record(mock_record._app, mock_record._raw)

        # Equality by id and app id
        assert record_copy == mock_record

        record_copy.id = '58ebb22807637a02d4a14bd7'

        assert record_copy != mock_record

        # Ordering by tracking id and app name
        record_copy.tracking_id = 'RA-16'
        assert mock_record < record_copy

        # Verify can't sort/order against non-record instances
        with pytest.raises(TypeError):
            mock_record < mock_app

    def test_unknown_field_access(self, mock_record):
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

    def test_iteration(self, mock_record):
        """Test that iterating over a record yields field names and their values like dict.items()"""
        num_fields = 0

        for field_name, field_value in mock_record:
            num_fields += 1
            assert field_value == mock_record[field_name]

        assert num_fields > 0
