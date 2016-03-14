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
        mock_cookie = {'.AspNet.ApplicationCookie': 'testcookie'}
        mock_requests.post.return_value.cookies = mock_cookie

        u = UserPassAuthProvider('server', 'user', 'pass')
        h = u.auth_header()

        self.assertEqual(h, {'Cookie': '.AspNet.ApplicationCookie=testcookie'})
        mock_requests.post.assert_called_once_with(
            'user/login',
            data={'username': 'user', 'password': 'pass'},
            verify=True)
        mock_requests.post.return_value.raise_for_status.assert_called_once_with()  # noqa
