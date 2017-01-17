from mock import patch
import unittest

from swimlane.core.auth.user_pass_auth_provider import UserPassAuthProvider


class UserPassAuthProviderTestCase(unittest.TestCase):
    def test_init(self):
        u = UserPassAuthProvider('server', 'user', 'pass')
        self.assertEqual(u.base_url, 'user/login')
        self.assertEqual(u.username, 'user')
        self.assertEqual(u.password, 'pass')
        self.assertEqual(u.verify_ssl, True)

    @patch('swimlane.core.auth.user_pass_auth_provider.requests', autospec=True)
    def test_auth_header(self, mock_requests):
        mock_cookie = {'.AspNetCore.Identity.Application': 'testcookie'}
        mock_requests.post.return_value.cookies = mock_cookie

        u = UserPassAuthProvider('server', 'user', 'pass')
        h = u.auth_header()

        self.assertEqual(h, {'Cookie': '.AspNetCore.Identity.Application=testcookie'})
        mock_requests.post.assert_called_once_with(
            'user/login',
            json={'username': 'user', 'password': 'pass'},
            verify=True)
        mock_requests.post.return_value.raise_for_status.assert_called_once_with()  # noqa

    @patch('swimlane.core.auth.user_pass_auth_provider.requests', autospec=True)
    def test_multiple_cookies(self, mock_requests):
        mock_requests.post.return_value.cookies = {
            'cookie_1': 'value_1',
            'cookie_2': 'value_2',
        }

        u = UserPassAuthProvider('server', 'user', 'pass')
        header = u.auth_header()

        self.assertIn('Cookie', header) 
        self.assertIn('cookie_1=value_1', header['Cookie'])
        self.assertIn('cookie_2=value_2', header['Cookie'])
        # test that cookies are separated with semicolon
        self.assertIn(';', header['Cookie'])

        mock_requests.post.assert_called_once_with(
            'user/login',
            json={'username': 'user', 'password': 'pass'},
            verify=True)
        mock_requests.post.return_value.raise_for_status.assert_called_once_with()  # noqa
