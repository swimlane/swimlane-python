import pytest

from swimlane.exceptions import ValidationError


def test_min_range(mock_record):
    """Test minimum range validation"""
    mock_record['Numeric (Range)'] = 0

    with pytest.raises(ValidationError):
        mock_record['Numeric (Range)'] = -1

    assert mock_record['Numeric (Range)'] == 0


def test_max_range(mock_record):
    """Test maximum range validation"""
    mock_record['Numeric (Range)'] = 10

    with pytest.raises(ValidationError):
        mock_record['Numeric (Range)'] = 11

    assert mock_record['Numeric (Range)'] == 10
