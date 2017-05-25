import mock

from swimlane.core.fields.reference import ReferenceCursor
from swimlane.core.resources import Record


class TestReferenceField(object):

    field_name = 'Reference'

    def test_target_app(self, mock_record, mock_swimlane, mock_app):
        """Test availability of .target_app property on ReferenceCursor"""

        field = mock_record.get_field(self.field_name)

        with mock.patch.object(mock_swimlane.apps, 'get', return_value=mock_app):

            assert field.target_app == mock_app

            reference_cursor = mock_record[self.field_name]
            assert isinstance(reference_cursor, ReferenceCursor)
            assert reference_cursor.target_app is field.target_app

    def test_lazy_retrieval(self, mock_app, mock_record):
        """Test lazy retrieval of referenced records"""
        # Can't patch attribute
        field = mock_record.get_field(self.field_name)
        field._ReferenceField__target_app = mock_app
        reference_cursor = mock_record[self.field_name]

        with mock.patch.object(reference_cursor.target_app.records, 'get') as mock_record_get:
            mock_record_get.return_value = mock_record
            assert mock_record_get.call_count == 0

            # Lazy retrieval of target app definition and selected records

            assert len(reference_cursor) == 3
            assert mock_record_get.call_count == 3

            for referenced_record in reference_cursor:
                assert isinstance(referenced_record, Record)

            # Add/remove/set referenced record(s) by Record instance or ID
            mock_record[self.field_name] = [mock_record]

            # Select/deselect
            assert len(mock_record[self.field_name]) == 1
            mock_record[self.field_name].remove(mock_record)
            assert len(mock_record[self.field_name]) == 0
            mock_record[self.field_name].add(mock_record)
            assert len(mock_record[self.field_name]) == 1

            # No new requests should have been necessary, other than the original lookups
            assert mock_record_get.call_count == 3

