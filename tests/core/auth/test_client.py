import mock
import unittest

from swimlane.core.auth import Client
from swimlane.core.auth.user_pass_auth_provider import UserPassAuthProvider
from swimlane.core.swimlane_dict import SwimlaneDict


class ClientTestCase(unittest.TestCase):
    def test_init(self):
        c = Client('server', 'user', 'pass')

        self.assertEqual(c.username, 'user')
        self.assertEqual(c.session.verify, True)
        self.assertEqual(c.base_url, 'api/')
        self.assertIsInstance(c.provider, UserPassAuthProvider)

    @mock.patch('swimlane.core.auth.client.UserPassAuthProvider', autospec=True)
    def test_connect(self, mock_provider):
        mock_cookie = {'Cookie': 'cookie=testcookie'}
        mock_provider.return_value.auth_header.return_value = mock_cookie

        c = Client('server', 'user', 'pass')
        c.connect()

        self.assertTrue(all(item in c.session.headers.items() for item in mock_cookie.items()))

    @mock.patch('swimlane.core.auth.client.UserPassAuthProvider', autospec=True)
    def test_set_default(self, mock_provider):
        Client.set_default('server', 'user', 'pass')
        mock_provider.return_value.auth_header.assert_called_once_with()

    def test_check_default_is_set(self):
        self.assertRaises(Exception, Client.check_default_is_set)

    def test_get(self):
        mock_response = mock.MagicMock()

        c = Client('server', 'user', 'pass')
        with mock.patch.object(c.session, 'get', return_value=mock_response) as mock_requests:
            c.get('test')

            mock_requests.assert_called_once_with(
                'api/test'
            )
            mock_response.raise_for_status.assert_called_once_with()

    def test_get_classmethod(self):
        mock_response = mock.MagicMock()

        Client.default = Client('server', 'user', 'pass')
        with mock.patch.object(Client.default.session, 'get', return_value=mock_response) as mock_requests:
            Client.get('test')

            mock_requests.assert_called_once_with(
                'api/test'
            )
            mock_response.raise_for_status.assert_called_once_with()

    def test_post(self):
        mock_response = mock.MagicMock()

        c = Client('server', 'user', 'pass')
        with mock.patch.object(c.session, 'post', return_value=mock_response) as mock_requests:
            c.post({}, 'test')

            mock_requests.assert_called_once_with(
                'api/test',
                json={}
            )
            mock_response.raise_for_status.assert_called_once_with()

    def test_post_classmethod(self):
        mock_response = mock.MagicMock()

        Client.default = Client('server', 'user', 'pass')
        with mock.patch.object(Client.default.session, 'post', return_value=mock_response) as mock_requests:
            Client.post({}, 'test')

            mock_requests.assert_called_once_with(
                'api/test',
                json={}
            )
            mock_response.raise_for_status.assert_called_once_with()

    def test_put(self):
        mock_response = mock.MagicMock()

        c = Client('server', 'user', 'pass')
        with mock.patch.object(c.session, 'put', return_value=mock_response) as mock_requests:

            c.put({}, 'test')

            mock_requests.assert_called_once_with(
                'api/test',
                json={}
            )
            mock_response.raise_for_status.assert_called_once_with()

    def test_put_classmethod(self):
        mock_response = mock.MagicMock()

        Client.default = Client('server', 'user', 'pass')
        with mock.patch.object(Client.default.session, 'put', return_value=mock_response) as mock_requests:
            Client.put({}, 'test')

            mock_requests.assert_called_once_with(
                'api/test',
                json={}
            )
            mock_response.raise_for_status.assert_called_once_with()

    def test_send_data(self):
        mock_requests = mock.MagicMock()

        c = Client('server', 'user', 'pass')
        c.send_data({}, 'test', mock_requests)

        mock_requests.assert_called_once_with(
            'api/test',
            json={},
        )
        mock_requests.return_value.raise_for_status.assert_called_once_with()

    def test_build_payload(self):
        mock_response = mock.MagicMock()
        c = Client('server', 'user', 'pass')

        mock_response.content = None
        self.assertEqual(c.build_payload(mock_response), None)

        mock_response.content = '{}'
        mock_response.json.return_value = {}
        self.assertIsInstance(c.build_payload(mock_response), SwimlaneDict)

        mock_response.content = '[{}]'
        mock_response.json.return_value = [{}]
        payload = c.build_payload(mock_response)
        self.assertIsInstance(next(payload), SwimlaneDict)
