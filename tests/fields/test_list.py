import pytest

from swimlane.exceptions import ValidationError


def test_getattr_fallback(mock_record):
    """Verify cursor __getattr__ falls back to AttributeError for unknown cursor + list methods"""
    with pytest.raises(AttributeError):
        getattr(mock_record['Text List'], 'unknown_method')


def test_set_validation(mock_record):
    """Test directly setting a ListField value for validation"""

    mock_record['Text List'] = ['text']

    with pytest.raises(ValidationError):
        mock_record['Text List'] = [123]

    with pytest.raises(ValidationError):
        mock_record['Text List'] = 123

    with pytest.raises(ValidationError):
        mock_record['Text List'] = 'text'


def test_modification_validation(mock_record):
    """Test calling list methods on cursor respects validation"""

    mock_record['Text List'].append('text')

    with pytest.raises(ValidationError):
        mock_record['Text List'].append(123)


def test_numeric_range(mock_record):
    """Test item numeric range restrictions"""

    key = 'Numeric List Range Limit'

    mock_record[key] = [5]

    with pytest.raises(ValidationError):
        mock_record[key] = [3]

    with pytest.raises(ValidationError):
        mock_record[key] = [12]


def test_list_length_validation(mock_record):
    """List length validation check"""
    key = 'Numeric List Range Limit'

    mock_record[key] = [5, 6, 7]

    with pytest.raises(ValidationError):
        mock_record[key].append(8)

    with pytest.raises(ValidationError):
        mock_record[key] = []


def test_item_type_validation(mock_record):
    """Validate correct item type for text/numeric values"""
    key = 'Numeric List Range Limit'

    with pytest.raises(ValidationError):
        mock_record[key] = ['text']


def test_min_max_word_validation(mock_record):
    """Validate against min/max word restrictions"""
    key = 'Text List Word Limit'

    with pytest.raises(ValidationError):
        mock_record[key] = ['word ' * 10]

    with pytest.raises(ValidationError):
        mock_record[key] = ['word']


def test_min_max_char_validation(mock_record):
    """Min/max characters restriction validation"""
    key = 'Text List Char Limit'

    with pytest.raises(ValidationError):
        mock_record[key] = ['defg', 'hijkl', 'mno pqr']

    with pytest.raises(ValidationError):
        mock_record[key] = ['']


def test_list_field_bulk_modify_value(mock_record):
    """Pass-through bulk_modify value"""
    value = ['Test', 'Value']
    assert mock_record.get_field('Text List').get_bulk_modify(value) == value
