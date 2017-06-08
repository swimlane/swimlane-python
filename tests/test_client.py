"""Tests for custom Swimlane errors"""
import mock
import pytest
from requests import HTTPError

from swimlane.core.client import SwimlaneAuth, Swimlane
from swimlane.exceptions import SwimlaneHTTP400Error, InvalidServerVersion


def test_request_handling(mock_swimlane):
    """Test error message and code for SwimlaneHTTP400Error class"""

    with mock.patch.object(mock_swimlane, '_session') as mock_session:
        mock_response = mock.MagicMock()

        # Test with non-400 error; Should return a standard HTTPError
        mock_response.status_code = 401
        mock_session.request.return_value.raise_for_status.side_effect = HTTPError(response=mock_response)

        try:
            mock_swimlane.request('get', '/somepage')
        except HTTPError as error:
            assert not isinstance(error, SwimlaneHTTP400Error)
        else:
            raise RuntimeError

        # Test various 400 response error codes and messages
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'ErrorCode': -1,
            'Argument': None
        }

        try:
            mock_swimlane.request('get', '/somepage')
        except SwimlaneHTTP400Error as error:
            assert error.code == -1
            assert error.name == 'Unknown'
            assert error.argument is None
        else:
            raise RuntimeError

        mock_response.json.return_value = {
            'Argument': 'argument',
            'ErrorCode': 3002
        }

        try:
            mock_swimlane.request('get', 'somepage')
        except SwimlaneHTTP400Error as error:
            assert error.code == 3002
            assert error.name == 'RecordNotFound'
            assert error.argument == 'argument'
        else:
            raise RuntimeError

        # Test failure to parse response content
        mock_response.json.side_effect = ValueError

        try:
            mock_swimlane.request('get', 'somepage')
        except SwimlaneHTTP400Error as error:
            assert error.code == -1
            assert error.name == 'Unknown'
            assert error.argument is None
        else:
            raise RuntimeError


def test_lazy_settings():
    """Test accessing settings is evaluated lazily and cached after first retrieval"""
    with mock.patch.object(Swimlane, 'request') as mock_request:
        with mock.patch.object(SwimlaneAuth, 'authenticate', return_value=(None, {})):
            mock_response = mock.MagicMock()
            mock_request.return_value = mock_response

            # Only include apiVersion setting for current tests
            data = {
                'apiVersion': '2.15.0-1234'
            }
            mock_response.json.return_value = data

            mock_swimlane = Swimlane('http://host', 'user', 'pass', verify_server_version=False)

            assert mock_request.call_count == 0

            assert mock_swimlane.settings == data
            assert mock_swimlane.version == data['apiVersion']

            assert mock_request.call_count == 1


def test_server_version_checks():
    """Test that server version is checked by default, raising InvalidServerVersion exception when failing"""
    with mock.patch('swimlane.core.client.requests.Session', mock.MagicMock()):
        with mock.patch.object(SwimlaneAuth, 'authenticate', return_value=(None, {})):
            with mock.patch.object(Swimlane, 'settings', new_callable=mock.PropertyMock) as mock_settings:
                mock_settings.return_value = {'apiVersion': '2.15.0'}

                with mock.patch('swimlane.core.client.compare_versions', return_value=0):
                    Swimlane('http://host', 'admin', 'password')

                with mock.patch('swimlane.core.client.compare_versions', return_value=1):
                    with pytest.raises(InvalidServerVersion):
                        Swimlane('http://host', 'admin', 'password')


def test_auth(mock_swimlane):
    """Test automatic auth request and header injection with automatic version handling"""
    with mock.patch.object(mock_swimlane._session, 'request') as mock_request:
        mock_response = mock.MagicMock()
        mock_request.return_value = mock_response

        # Swimlane v2.13-
        mock_response.json.return_value = {
            '$type': 'API.Models.Identity.AuthorizeModel, API',
            'active': False,
            'createdByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core'},
            'createdDate': '2017-03-31T09:10:52.717Z',
            'disabled': False,
            'displayName': 'admin',
            'groups': [{'$type': 'Core.Models.Base.Entity, Core',
                        'disabled': False,
                        'id': '58de1d1c07637a0264c0ca71',
                        'name': 'Everyone'}],
            'id': '58de1d1c07637a0264c0ca6a',
            'isAdmin': True,
            'isMe': True,
            'lastLogin': '2017-04-27T14:11:38.54Z',
            'lastPasswordChangedDate': '2017-03-31T09:10:52.536Z',
            'modifiedByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core'},
            'modifiedDate': '2017-03-31T09:10:52.76Z',
            'name': 'admin',
            'passwordComplexityScore': 3,
            'passwordResetRequired': False,
            'permission': {'$type': 'Core.Models.Security.PermissionMatrix, Core'},
            'roles': [{'$type': 'Core.Models.Base.Entity, Core',
                       'disabled': False,
                       'id': '58de1d1c07637a0264c0ca64',
                       'name': 'Administrator'}],
            'userName': 'admin',
            'users': []}

        mock_response.cookies.items.return_value = [('.AspNetCore.Identity.Application',
                                                     'CfDJ8Eq07zdLE8ZGtPyzBNIkJhIgJB4-EUThghuYsSpPGU6fiO0uXHSfU2LDOmrpxmfa8KAVjMI1JSL1YyXzCXavaTMT7ZBwUO9J6rJG3m2p3B8hHFMd4RGRQypqP-znY6VEJmrvVr6_ZSF8sx-E54FI2N5WQo7gfiqGVIX70WrqyTvbaU1spoGsTRsXs1BJaUeobhSrI8MWjouqXSDuhcTJjjGczq_LGlBkdzYpV1wzPJSiwWXs-ZN2pIJzfMOedAJRs0OzIvVbB8aUn0zKfUu5K3QHhKImdudDqsEadGtTLccygC6t9b6XqIueMGuOYnn7mmOUv6MJBwdzTCfh2Eg4ElYOB8pqZsedWSbXz1GYuTlTpLWihJTwADMKtucIX1myfM4M9DVng_P9yp6K2BHm9_2jEcGJhnJQ2zJBML8TpRpdwhzz3iKBhBohFPqudEJ535zaR4onSO7dFGwbfx-fyZ5E31BNGl70A--y3VcNHeDqzs13ylpR--4DykUTGRnoYjsDFuD4ZHopvNGA8aC0LszaYeVW0M0aUzKw8VbiJdB3xQr9u6wkwscdzG3DqmJGgA')]

        auth = SwimlaneAuth(mock_swimlane, 'admin', 'password')

        assert auth._login_headers == {
            'Cookie': '.AspNetCore.Identity.Application=CfDJ8Eq07zdLE8ZGtPyzBNIkJhIgJB4-EUThghuYsSpPGU6fiO0uXHSfU2LDOmrpxmfa8KAVjMI1JSL1YyXzCXavaTMT7ZBwUO9J6rJG3m2p3B8hHFMd4RGRQypqP-znY6VEJmrvVr6_ZSF8sx-E54FI2N5WQo7gfiqGVIX70WrqyTvbaU1spoGsTRsXs1BJaUeobhSrI8MWjouqXSDuhcTJjjGczq_LGlBkdzYpV1wzPJSiwWXs-ZN2pIJzfMOedAJRs0OzIvVbB8aUn0zKfUu5K3QHhKImdudDqsEadGtTLccygC6t9b6XqIueMGuOYnn7mmOUv6MJBwdzTCfh2Eg4ElYOB8pqZsedWSbXz1GYuTlTpLWihJTwADMKtucIX1myfM4M9DVng_P9yp6K2BHm9_2jEcGJhnJQ2zJBML8TpRpdwhzz3iKBhBohFPqudEJ535zaR4onSO7dFGwbfx-fyZ5E31BNGl70A--y3VcNHeDqzs13ylpR--4DykUTGRnoYjsDFuD4ZHopvNGA8aC0LszaYeVW0M0aUzKw8VbiJdB3xQr9u6wkwscdzG3DqmJGgA'}

        mock_inflight_request = mock.MagicMock()
        auth(mock_inflight_request)
        mock_inflight_request.headers.update.assert_called_once_with(auth._login_headers)

        # Swimlane v2.14+
        JWT_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiJhTHFfcWlCWVJyVThoIiwidW5pcXVlX25hbWUiOiJhZG1pbiIsIm5iZiI6MTQ5MzMzMTQyNCwiZXhwIjoxNDkzMzM1MDI0LCJpYXQiOjE0OTMzMzE0MjQsImlzcyI6IlN3aW1sYW5lIiwiYXVkIjoiU3dpbWxhbmUifQ.w27D6JgYj6UuoTUivUmwNv8USqeieTTPwmmhJviiDRQ'

        mock_response.json.return_value = {
            '$type': 'API.Models.Identity.AuthorizeModel, API',
            'active': False,
            'createdByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core'},
            'createdDate': '2017-04-12T21:32:30.345Z',
            'disabled': False,
            'displayName': 'admin',
            'email': '',
            'favorites': {
                '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Collections.Generic.List`1[[System.String, mscorlib]], mscorlib]], mscorlib'},
            'groups': [{'$type': 'Core.Models.Base.Entity, Core',
                        'disabled': False,
                        'id': 'aLq_qiBYSzR1R',
                        'name': 'Everyone'}],
            'id': 'aLq_qiBYRrU8h',
            'isAdmin': True,
            'isMe': True,
            'lastLogin': '2017-04-27T16:17:04.5160226-06:00',
            'lastPasswordChangedDate': '2017-04-12T21:32:30.083Z',
            'modifiedByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core',
                               'id': 'aLq_qiBYRrU8h',
                               'name': 'admin'},
            'modifiedDate': '2017-04-27T22:17:04.5170289Z',
            'name': 'admin',
            'passwordResetRequired': False,
            'permission': {'$type': 'Core.Models.Security.PermissionMatrix, Core'},
            'roles': [{'$type': 'Core.Models.Base.Entity, Core',
                       'disabled': False,
                       'id': 'aLq_qiBYR2CvJ',
                       'name': 'Administrator'}],
            'token': JWT_TOKEN,
            'userName': 'admin',
            'users': []}

        auth = SwimlaneAuth(mock_swimlane, 'admin', 'password')

        assert auth._login_headers == {'Authorization': 'Bearer {}'.format(JWT_TOKEN)}

        mock_inflight_request = mock.MagicMock()
        auth(mock_inflight_request)
        mock_inflight_request.headers.update.assert_called_once_with(auth._login_headers)


def test_repr(mock_swimlane):
    assert repr(mock_swimlane) == '<Swimlane: admin @ http://host>'
