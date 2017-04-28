import mock
import pytest

from swimlane.core.resources import Group, User


def test_group_list(mock_group, mock_swimlane):
    mock_response = mock.MagicMock()
    mock_response.json.return_value = {'groups': [mock_group._raw for _ in range(3)]}

    with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
        groups = mock_swimlane.groups.list()
        assert len(groups) == 3
        for group in groups:
            assert isinstance(group, Group)


def test_group_get(mock_group, mock_swimlane):
    mock_response = mock.MagicMock()

    with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
        mock_response.json.return_value = mock_group._raw

        group = mock_swimlane.groups.get(id=mock_group.id)
        assert isinstance(group, Group)

        mock_response.json.return_value = [mock_group._raw]

        group = mock_swimlane.groups.get(name=mock_group.name)
        assert isinstance(group, Group)

        mock_response.json.return_value = []
        with pytest.raises(ValueError):
            mock_swimlane.groups.get(name=mock_group.name)


@pytest.mark.parametrize('kwargs', [
    {'unknown_arg': 'arg'},
    {'name': 'name', 'id': 'id'},
    {}
])
def test_group_get_invalid_args(mock_swimlane, kwargs):
    with pytest.raises(TypeError):
        mock_swimlane.groups.get(**kwargs)


def test_user_list(mock_user, mock_swimlane):
    mock_response = mock.MagicMock()
    mock_response.json.return_value = {'users': [mock_user._raw for _ in range(3)]}

    with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
        users = mock_swimlane.users.list()
        assert len(users) == 3
        for user in users:
            assert isinstance(user, User)


def test_user_get(mock_user, mock_swimlane):
    mock_response = mock.MagicMock()

    with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
        mock_response.json.return_value = mock_user._raw
        user = mock_swimlane.users.get(id=mock_user.id)
        assert user == mock_user

        mock_response.json.return_value = [mock_user._raw]
        user = mock_swimlane.users.get(username=mock_user.username)
        assert user == mock_user

        mock_response.json.return_value = []
        with pytest.raises(ValueError):
            mock_swimlane.users.get(username=mock_user.username)


@pytest.mark.parametrize('kwargs', [
    {'unknown_arg': 'arg'},
    {'username': 'name', 'id': 'id'},
    {}
])
def test_user_get_invalid_args(mock_swimlane, kwargs):
    with pytest.raises(TypeError):
        mock_swimlane.users.get(**kwargs)
