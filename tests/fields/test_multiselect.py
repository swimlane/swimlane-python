"""Tests for multiselect fields"""
from swimlane.core.resources import UserGroup
from swimlane.exceptions import ValidationError


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
    assert repr(mock_record['Values List']) == '<MultiSelectCursor: RA-7 (2)>'


def test_usergroup_single_field(mock_record, mock_group, mock_user):
    """Test single-select UserGroupField"""

    # Get usergroup from UserGroupField
    usergroup = mock_record['Incident Owner']

    assert isinstance(usergroup, UserGroup)
    assert usergroup.id == '58de1d1c07637a0264c0ca71'
    assert usergroup.name == 'Everyone'

    # UserGroup comparisons with specific User/Group instances
    assert usergroup == mock_group

    # Set User, Group, or UserGroup
    mock_record['Incident Owner'] = mock_user
    assert mock_record['Incident Owner'] == mock_user

    try:
        mock_record['Incident Owner'] = 'Everyone'
    except ValidationError:
        pass
    else:
        raise RuntimeError

    assert mock_record['Incident Owner'] == mock_user


def test_usergroup_multi_field(mock_record, mock_group, mock_user):
    """Test multi-select UserGroupField"""

    field_name = 'User/Groups'

    orig_value = mock_record[field_name]

    mock_record[field_name] = [mock_group, mock_user]

    assert list(mock_record[field_name]) == [mock_group, mock_user]

    mock_record[field_name] = orig_value


def test_usergroup_from_report(mock_record):
    """Test workaround for extraneous data returned from report without any selected users/groups on a multiselect field"""

    field_name = 'User/Groups'

    field = mock_record._fields[field_name]

    field.set_swimlane([{'$type': 'Core.Models.Utilities.UserGroupSelection, Core'}])

    assert list(mock_record[field_name]) == []
