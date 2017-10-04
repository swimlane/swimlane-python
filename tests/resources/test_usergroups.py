import pytest
from mock import patch

from swimlane.core.resources.usergroup import UserGroup


class TestUserGroups(object):

    def test_get_usergroup_selection(self, mock_user, mock_group):
        assert mock_user.as_usergroup_selection() == {
            '$type': 'Core.Models.Utilities.UserGroupSelection, Core',
            'id': '58de1d1c07637a0264c0ca6a',
            'name': 'admin'
        }

        assert mock_group.as_usergroup_selection() == {
            '$type': 'Core.Models.Utilities.UserGroupSelection, Core',
            'id': '58de1d1c07637a0264c0ca71',
            'name': 'Everyone'
        }

    def test_metamethods(self, mock_user, mock_group, mock_record):
        """Test handful of simple metamethods for id and hashing, sorting, uniqueness, etc."""
        # Equality by id
        assert mock_user != mock_group

        # Ordering by name (Everyone < admin)
        assert mock_group < mock_user

        # Ordering type support
        with pytest.raises(TypeError):
            mock_user < mock_record

        # Hash
        local_set = set()
        local_set.add(mock_user)

        assert mock_user in local_set

        local_set.add(mock_user)

        assert len(local_set) == 1

        # Str
        assert str(mock_user) == mock_user.name

    def test_resolve(self, mock_swimlane, mock_user, mock_group):
        """Test resolving a generic UserGroup to more specific type"""
        ug_user = UserGroup(mock_user._swimlane, mock_user._raw)
        ug_group = UserGroup(mock_group._swimlane, mock_group._raw)

        # Test resolve is no-op when already resolved
        for ug in (mock_user, mock_group):
            assert ug.resolve() is ug

        with patch.object(mock_swimlane.users, 'get') as mock_user_get:
            with patch.object(mock_swimlane.groups, 'get') as mock_group_get:
                mock_group_get.return_value = mock_group
                mock_user_get.return_value = mock_user

                assert ug_user.resolve() is mock_user

                mock_user_get.side_effect = ValueError

                assert ug_group.resolve() is mock_group
