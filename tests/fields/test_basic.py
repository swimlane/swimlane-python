"""Tests for basic fields without substantial logic"""
import numbers

import pytest

from swimlane.core.fields import resolve_field_class, _FIELD_TYPE_MAP
from swimlane.core.fields.base import ReadOnly, FieldCursor
from swimlane.exceptions import ValidationError


def test_text_field(mock_record):
    """Test automatic type coercion during set"""

    assert mock_record['Severity'] == '7'
    mock_record['Severity'] = int(mock_record['Severity']) + 1
    assert mock_record['Severity'] == '8'


def test_numeric_field(mock_record):
    """Test type validation"""

    assert isinstance(mock_record['Numeric'], numbers.Number)

    with pytest.raises(ValidationError):
        mock_record['Numeric'] = 'Not a number'

    current_value = mock_record['Numeric']
    mock_record['Numeric'] += 1
    assert mock_record['Numeric'] == current_value + 1


def test_tracking_id_field(mock_record):
    """Test Tracking Id is readonly"""

    assert mock_record['Tracking Id'] == 'RA-7'

    with pytest.raises(ValidationError):
        mock_record['Tracking Id'] = 'Other Tracking value'


def test_default_repr(mock_record):
    assert repr(mock_record._fields['Numeric']) == '<NumberField: 1>'


def test_resolve_field_class():
    """Test looking up field by field $type"""
    with pytest.raises(KeyError):
        resolve_field_class({'$type': 'Not a valid type'})


@pytest.mark.parametrize(
    'field_class',
    [cls for cls in _FIELD_TYPE_MAP.values() if not issubclass(cls, ReadOnly)]
)
def test_all_fields_empty_value(mock_record, field_class):
    """Test setting fields to empty value works for all field classes"""
    # Get any not readonly field instance of provided field_class
    # Does not guarantee full scope of all field subtypes function as expected
    field = next((_field for _field in mock_record._fields.values() if isinstance(_field, field_class) and not _field.readonly))

    del mock_record[field.name]

    swimlane = field.get_swimlane()
    python = field.get_python()

    if getattr(field, 'is_multiselect', False) or isinstance(python, FieldCursor):
        # Multi select fields use cursors or ordered sets in most cases
        assert len(swimlane) == len(python) == 0
    else:
        assert swimlane is python is None
