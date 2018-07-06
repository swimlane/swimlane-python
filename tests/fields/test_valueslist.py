
def test_values_list_single_select_field(mock_record):
    """Test a ValuesList field in single-select mode"""
    assert mock_record['Status'] == 'Open'

    # Attempt to set value to invalid option
    try:
        mock_record['Status'] = 'Not valid'
    except ValueError:
        assert mock_record['Status'] == 'Open'
    else:
        raise RuntimeError

    # Set to valid option
    mock_record['Status'] = 'Closed'
    assert mock_record['Status'] == 'Closed'


def test_values_list_multi_select_field(mock_record):
    """Test a ValuesList field in multi-select mode"""
    vl_cursor = mock_record['Values List']
    assert len(vl_cursor) == 2

    # Adding the same value multiple times is ignored
    vl_cursor.select('Option 3')
    assert len(vl_cursor) == 3
    vl_cursor.select('Option 3')
    assert len(vl_cursor) == 3

    # Get item by index
    assert vl_cursor[0] == 'Option 1'
    assert vl_cursor[2] == 'Option 3'

    # Remove element raises exception if not already added
    vl_cursor.deselect('Option 3')
    assert len(vl_cursor) == 2

    try:
        vl_cursor.deselect('Option 3')
    except KeyError:
        assert len(vl_cursor) == 2
    else:
        raise RuntimeError

    # Respects field's valid options and types, raising ValueError for invalid values
    try:
        vl_cursor.select('Not a valid option')
    except ValueError:
        assert len(vl_cursor) == 2
    else:
        raise RuntimeError

    # Field can be set directly to any iterable, overwriting current selection entirely
    # Also resets field to a fresh cursor on next access
    vl_original_values = list(mock_record['Values List'])
    mock_record['Values List'] = []
    assert len(mock_record['Values List']) == 0

    # All elements must pass validation, or entire set operation fails
    try:
        mock_record['Values List'] = ['Option 1', 'Not a valid option']
    except ValueError:
        pass
    else:
        raise RuntimeError

    assert len(mock_record['Values List']) == 0
    mock_record['Values List'] = vl_original_values
    assert len(mock_record['Values List']) == 2

    # Attempt to directly set to a non-iterable value
    try:
        mock_record['Values List'] = 'Option 1'
    except ValueError:
        pass
    else:
        raise RuntimeError


def test_cursor_repr(mock_record):
    assert repr(mock_record['Values List']) == '<MultiSelectCursor: <Record: RA-7>["Values List"] (2)>'


def test_get_report(mock_record):
    """Test behavior of values list get_report()"""
    field = mock_record.get_field('Values List')

    assert field.get_report(field.get_python()) == [
        '58fae4c59173122945a7cff6',
        '58fae4eafef0eead26dee65c'
    ]
