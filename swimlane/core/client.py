import weakref

import requests
from six.moves.urllib.parse import urljoin
from pyuri import URI

from swimlane.core.resources.app import AppAdapter


class SwimlaneAuth(object):

    def __init__(self, swimlane):
        self.swimlane = weakref.proxy(swimlane)
        self.login_headers = self._authenticate()

    def __call__(self, request):

        request.headers.update(self.login_headers)

        return request

    def _authenticate(self):
        """Send login request and return login token"""
        resp = self.swimlane.api('post', 'user/login', json={
            'userName': self.swimlane.username,
            'password': self.swimlane.password,
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


class Swimlane(object):
    """Swimlane API driver"""

    _api_root = '/api/'

    def __init__(self, host, username, password, verify_ssl=True):
        self.host = URI(host)
        self.host.scheme = self.host.scheme or 'https'
        self.host.path = None

        self.username = username
        self.password = password

        self.session = requests.Session()
        self.session.verify = verify_ssl
        self.session.auth = SwimlaneAuth(self)

        self.apps = AppAdapter(self)

    def api(self, method, endpoint, **kwargs):
        """Shortcut helper for sending requests to API endpoints"""
        while endpoint.startswith('/'):
            endpoint = endpoint[1:]

        response = self.session.request(method, urljoin(str(self.host) + self._api_root, endpoint), **kwargs)
        response.raise_for_status()

        return response
