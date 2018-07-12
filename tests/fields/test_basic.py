"""Tests for basic fields without substantial logic"""
import numbers

import pytest
import six

from swimlane.core.fields import resolve_field_class, _FIELD_TYPE_MAP, Field, _build_field_type_map
from swimlane.core.fields.base import ReadOnly, FieldCursor
from swimlane.core.fields.list import ListField
from swimlane.exceptions import ValidationError
from swimlane.utils import get_recursive_subclasses


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
    # Check for error on known invalid type
    with pytest.raises(KeyError):
        resolve_field_class({'$type': 'Not a valid type'})

    # Check all fields with a type are resolvable by their types
    for cls in get_recursive_subclasses(Field):
        if cls.field_type:
            if isinstance(cls.field_type, six.string_types):
                types = [cls.field_type]
            else:
                types = cls.field_type

            for field_type in types:
                assert resolve_field_class({'$type': field_type}) is cls


def test_error_on_invalid_field_type():
    """Make sure an exception is raised when building type map if field_type is not a tuple or string"""
    class Base(object):
        field_type = None

    class Invalid(Base):
        field_type = 12345

    with pytest.raises(ValueError):
        _build_field_type_map(Base)


@pytest.mark.parametrize(
    'field_class',
    [cls for cls in _FIELD_TYPE_MAP.values() if not (issubclass(cls, ReadOnly) or cls == ListField)]
)
def test_all_fields_empty_value(mock_record, field_class):
    """Test setting fields to empty value works for all field classes"""
    # Get any not readonly field instance of provided field_class
    # Does not guarantee full scope of all field subtypes function as expected
    for field in mock_record._fields.values():
        if isinstance(field, field_class) and not field.readonly:
            del mock_record[field.name]

            swimlane = field.get_swimlane()
            python = field.get_python()
            if getattr(field, 'is_multiselect', False) or isinstance(python, FieldCursor):
                # Multi select fields use cursors or ordered sets in most cases
                assert swimlane is None
                assert len(python) == 0

            else:
                assert swimlane is python is None
