import mock
import pytest


def test_get(mock_swimlane, mock_app):
    mock_response = mock.MagicMock()

    with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):

        mock_response.status_code = 200
        mock_response.json.return_value = mock_app._raw

        assert mock_swimlane.apps.get(id=mock_app.id).id == mock_app.id

        mock_response.json.return_value = [mock_app._raw]

        assert mock_swimlane.apps.get(name=mock_app.name).id == mock_app.id
        mock_response.json.return_value = []

        with pytest.raises(ValueError):
            mock_swimlane.apps.get(name=mock_app.name)

        mock_response.status_code = 204

        with pytest.raises(ValueError):
            mock_swimlane.apps.get(id=mock_app.id)


@pytest.mark.parametrize('kwargs', [
    {'unknown_arg': 'arg'},
    {'name': 'name', 'id': 'id'},
    {}
])
def test_invalid_args(mock_swimlane, kwargs):
    with pytest.raises(TypeError):
        mock_swimlane.apps.get(**kwargs)
