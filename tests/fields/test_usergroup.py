import pytest

from swimlane.core.resources.usergroup import UserGroup
from swimlane.exceptions import ValidationError


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
