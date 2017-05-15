import mock

from swimlane.core.fields.reference import ReferenceCursor
from swimlane.core.resources import Record


def test_reference_field(mock_record, mock_swimlane, mock_app):

    field_name = 'Reference'

    field = mock_record._fields[field_name]

    record_id = '58e24e8607637a0b488849d4'

    with mock.patch.object(mock_swimlane.apps, 'get', return_value=mock_app):

        assert field.target_app == mock_app

        reference = mock_record[field_name]
        assert isinstance(reference, ReferenceCursor)
        assert reference.target_app is field.target_app

    with mock.patch.object(mock_app.records, 'get', return_value=mock_record):
        # Lazy retrieval of target app definition and selected records

        assert len(reference) == 3

        for referenced_record in reference:
            assert isinstance(referenced_record, Record)

        # Add/remove/set referenced record(s) by Record instance or ID
        mock_record[field_name] = [record_id]
        mock_record[field_name] = [mock_record]

        # Select/deselect
        assert len(mock_record[field_name]) == 1
        mock_record[field_name].deselect(mock_record)
        assert len(mock_record[field_name]) == 0
        mock_record[field_name].select(mock_record)
        assert len(mock_record[field_name]) == 1

