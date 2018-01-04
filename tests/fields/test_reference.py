import mock
import pytest

from swimlane.core.fields.reference import ReferenceCursor
from swimlane.core.resources.record import Record
from swimlane.core.resources.app import App
from swimlane.exceptions import ValidationError, SwimlaneHTTP400Error


class TestReferenceField(object):

    multi_field_name = 'Reference'
    single_field_name = 'Reference (Select Single)'

    def test_target_app(self, mock_record, mock_swimlane, mock_app):
        """Test availability of .target_app property on ReferenceCursor"""

        field = mock_record.get_field(self.multi_field_name)

        with mock.patch.object(mock_swimlane.apps, 'get', return_value=mock_app):

            assert field.target_app == mock_app

            reference_cursor = mock_record[self.multi_field_name]
            assert isinstance(reference_cursor, ReferenceCursor)
            assert reference_cursor.target_app is field.target_app

    def test_single_select(self, mock_swimlane, mock_record):
        """Test single-select get/set"""

        with mock.patch.object(mock_swimlane.apps, 'get', return_value=mock_record.app):
            field = mock_record.get_field(self.single_field_name)

            assert field.get_python() is None

            # Assert setting to None adds the field's key to raw values
            field.set_python(None)
            assert mock_record._raw['values'][field.id] is None

            field.set_python(mock_record)
            assert mock_record._raw['values'][field.id] == mock_record.id

            field.set_swimlane(mock_record.id)
            assert mock_record.id in field._value

    def test_empty_multi_select(self, mock_record):
        """Test empty multi select reference field"""

        field = mock_record.get_field('Reference')
        mock_record['Reference'] = None
        swimlane = field.get_swimlane()
        python = field.get_python()
        assert swimlane is None
        assert len(python) == 0

    def test_lazy_retrieval(self, mock_app, mock_record):
        """Test lazy retrieval of referenced records"""
        # Can't patch attribute
        field = mock_record.get_field(self.multi_field_name)
        field._ReferenceField__target_app = mock_app
        reference_cursor = mock_record[self.multi_field_name]

        with mock.patch.object(reference_cursor.target_app.records, 'get') as mock_record_get:
            mock_record_get.return_value = mock_record
            assert mock_record_get.call_count == 0

            # Lazy retrieval of target app definition and selected records

            assert len(reference_cursor) == 3
            assert mock_record_get.call_count == 3

            for referenced_record in reference_cursor:
                assert isinstance(referenced_record, Record)

            # Add/remove/set referenced record(s) by Record instance or ID
            mock_record[self.multi_field_name] = [mock_record]

            # Select/deselect
            assert len(mock_record[self.multi_field_name]) == 1
            mock_record[self.multi_field_name].remove(mock_record)
            assert len(mock_record[self.multi_field_name]) == 0
            mock_record[self.multi_field_name].add(mock_record)
            assert len(mock_record[self.multi_field_name]) == 1

            # No new requests should have been necessary, other than the original lookups
            assert mock_record_get.call_count == 3

    def test_target_app_validation(self, mock_swimlane, mock_record, mock_app):
        """Test that reference field validation checks that provided record is in the field's target app"""
        # Set target app to some random other app
        target_app = App(mock_swimlane, mock_app._raw)
        target_app.id = 'abcdef'
        target_app.name = 'Some other app'

        with mock.patch.object(mock_swimlane.apps, 'get', return_value=target_app):
            reference_cursor = mock_record[self.multi_field_name]

            with pytest.raises(ValidationError):
                reference_cursor.add(mock_record)

            with pytest.raises(ValidationError):
                mock_record[self.multi_field_name] = [mock_record]

    def test_orphaned_record_cleanup(self, mock_swimlane, mock_record, mock_app):
        """Test that orphaned records that no longer exist are ignored by ReferenceCursor"""
        mock_response = mock.MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'ErrorCode': 3002,
            'Argument': None
        }

        with mock.patch.object(mock_swimlane.apps, 'get', return_value=mock_app):
            with mock.patch.object(mock_app.records, 'get', side_effect=SwimlaneHTTP400Error(mock_response)):
                assert len(mock_record[self.multi_field_name]) == 0

    def test_get_report(self, mock_record):
        """All for total coverage"""
        assert mock_record.get_field(self.single_field_name).get_report(mock_record) == mock_record.id
