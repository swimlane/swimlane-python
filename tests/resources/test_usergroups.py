import pytest


class TestUserGroups(object):

    def test_get_usergroup_selection(self, mock_user, mock_group):
        assert mock_user.get_usergroup_selection() == {
            '$type': 'Core.Models.Utilities.UserGroupSelection, Core',
            'id': '58de1d1c07637a0264c0ca6a',
            'name': 'admin'
        }

        assert mock_group.get_usergroup_selection() == {
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
