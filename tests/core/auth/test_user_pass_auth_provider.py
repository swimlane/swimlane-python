from mock import patch, MagicMock, Mock
import unittest

from swimlane.core.auth.user_pass_auth_provider import UserPassAuthProvider


class UserPassAuthProviderTestCase(unittest.TestCase):
    def test_init(self):
        u = UserPassAuthProvider('server', 'user', 'pass')
        self.assertEqual(u.base_url, 'user/login')
        self.assertEqual(u.username, 'user')
        self.assertEqual(u.password, 'pass')

    def test_auth_header(self):
        mock_cookie = {'.AspNetCore.Identity.Application': 'testcookie'}
        mock_session = MagicMock()
        mock_session.post.return_value.json.return_value = {}
        mock_session.post.return_value.cookies = mock_cookie

        u = UserPassAuthProvider('server', 'user', 'pass', mock_session)
        h = u.auth_header()

        self.assertEqual(h, {'Cookie': '.AspNetCore.Identity.Application=testcookie'})
        mock_session.post.assert_called_once_with(
            'user/login',
            json={'username': 'user', 'password': 'pass'}
        )
        mock_session.post.return_value.raise_for_status.assert_called_once_with()  # noqa

    def test_multiple_cookies(self):
        mock_session = Mock()

        mock_session.post.return_value.json.return_value = {}
        mock_session.post.return_value.cookies = {
            'cookie_1': 'value_1',
            'cookie_2': 'value_2',
        }

        u = UserPassAuthProvider('server', 'user', 'pass', mock_session)
        header = u.auth_header()

        self.assertIn('Cookie', header) 
        self.assertIn('cookie_1=value_1', header['Cookie'])
        self.assertIn('cookie_2=value_2', header['Cookie'])
        # test that cookies are separated with semicolon
        self.assertIn(';', header['Cookie'])

        mock_session.post.assert_called_once_with(
            'user/login',
            json={'username': 'user', 'password': 'pass'},
        )
        mock_session.post.return_value.raise_for_status.assert_called_once_with()  # noqa

    def test_jwt_headers(self):
        mock_session = MagicMock()

        mock_session.post.return_value.json.return_value = {
            'token': 'token'
        }

        u = UserPassAuthProvider('server', 'user', 'pass', mock_session)
        header = u.auth_header()

        self.assertEqual(header['Authorization'], 'Bearer token')

        mock_session.post.assert_called_once_with(
            'user/login',
            json={'username': 'user', 'password': 'pass'},
        )
        mock_session.post.return_value.raise_for_status.assert_called_once_with()  # noqa
