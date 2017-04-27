"""Tests for basic fields without substantial logic"""
import numbers

import pytest


def test_text_field(mock_record):
    """Test automatic type coercion during set"""

    assert mock_record['Severity'] == '7'
    mock_record['Severity'] = int(mock_record['Severity']) + 1
    assert mock_record['Severity'] == '8'


def test_numeric_field(mock_record):
    """Test type validation"""

    assert isinstance(mock_record['Numeric'], numbers.Number)

    with pytest.raises(TypeError):
        mock_record['Numeric'] = 'Not a number'

    current_value = mock_record['Numeric']
    mock_record['Numeric'] += 1
    assert mock_record['Numeric'] == current_value + 1


def test_tracking_id_field(mock_record):
    """Test Tracking Id is readonly"""

    assert mock_record['Tracking Id'] == 'RA-7'

    with pytest.raises(AttributeError):
        mock_record['Tracking Id'] = 'Other Tracking value'