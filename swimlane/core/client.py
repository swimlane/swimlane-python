import weakref

import requests
from six.moves.urllib.parse import urljoin
from pyuri import URI

from swimlane.core.resources.app import AppAdapter
from swimlane.core.resources.user import UserAdapter


class Swimlane(object):
    """Swimlane API client"""

    _api_root = '/api/'

    def __init__(self, host, username, password, verify_ssl=True):
        self.host = URI(host)
        self.host.scheme = self.host.scheme or 'https'
        self.host.path = None

        self.session = requests.Session()
        self.session.verify = verify_ssl
        self.session.auth = SwimlaneAuth(self, username, password)

        self.apps = AppAdapter(self)
        self.users = UserAdapter(self)

        self.__settings = None
        self.__user = None

    def request(self, method, endpoint, **kwargs):
        """Shortcut helper for sending requests to API endpoints
        
        Handles generating full API URL, session reuse and auth, and response status code checks
        """
        while endpoint.startswith('/'):
            endpoint = endpoint[1:]

        response = self.session.request(method, urljoin(str(self.host) + self._api_root, endpoint), **kwargs)
        response.raise_for_status()

        return response

    @property
    def settings(self):
        """Retrieve and cache settings from server"""
        if not self.__settings:
            self.__settings = self.request('get', 'settings').json()
        return self.__settings

    @property
    def version(self):
        """Returns server API version"""
        return self.settings['apiVersion']

    @property
    def user(self):
        """Returns User record for authenticated user"""
        if not self.__user:
            self.__user = self.users.get(username=self.session.auth.username)
        return self.__user


class SwimlaneAuth(object):

    def __init__(self, swimlane, username, password):
        self.username = username
        self.password = password

        self._swimlane = weakref.proxy(swimlane)
        self._login_headers = self._authenticate()

    def __call__(self, request):

        request.headers.update(self._login_headers)

        return request

    def _authenticate(self):
        """Send login request and return login token"""
        resp = self._swimlane.request('post', 'user/login', json={
            'userName': self.username,
            'password': self.password,
            'domain': ''
        })
        json_content = resp.json()

        # Check for token in response content
        token = json_content.get('token')

        if token is None:
            # Legacy cookie authentication (2.13-)
            headers = {'Cookie': ';'.join(
                ["%s=%s" % cookie for cookie in resp.cookies.items()]
            )}
        else:
            # JWT auth (2.14+)
            headers = {
                'Authorization': 'Bearer {}'.format(token)
            }

        return headers
