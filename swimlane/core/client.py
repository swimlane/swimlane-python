import re
import weakref

import requests
from pyuri import URI
from requests import HTTPError
from six.moves.urllib.parse import urljoin

from swimlane.core.resources.app import AppAdapter
from swimlane.core.resources.usergroup import UserAdapter, GroupAdapter
# from swimlane.core.resources.tasks import TaskAdapter
from swimlane.errors import SwimlaneError


class Swimlane(object):
    """Swimlane API client"""

    _api_root = '/api/'

    def __init__(self, host, username, password, verify_ssl=True):
        self.host = URI(host)
        self.host.scheme = self.host.scheme or 'https'
        self.host.path = None

        self._session = requests.Session()
        self._session.verify = verify_ssl
        self._session.headers = {
            'Content-Type': 'application/json'
        }
        self._session.auth = SwimlaneAuth(self, username, password)

        self.apps = AppAdapter(self)
        self.users = UserAdapter(self)
        self.groups = GroupAdapter(self)

        self.__settings = None
        self.__user = None

    def request(self, method, endpoint, **kwargs):
        """Shortcut helper for sending requests to API endpoints
        
        Handles generating full API URL, session reuse and auth, and response status code checks
        
        Raises HTTPError on 4xx/5xx HTTP responses, or SwimlaneError on 400 responses with 
        """
        while endpoint.startswith('/'):
            endpoint = endpoint[1:]

        response = self._session.request(method, urljoin(str(self.host) + self._api_root, endpoint), **kwargs)

        try:
            response.raise_for_status()
        except HTTPError as e:
            if e.response.status_code == 400:
                raise SwimlaneError(e)
            else:
                raise

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
            self.__user = self.users.get(username=self._session.auth.username)
        return self.__user

    def _compare_version(self, *version_sections):
        """Return direction of Swimlane version relative to provided version sections
        
        If Swimlane version is equal to provided version, return 0
        If Swimlane version is greater than provided version, return 1
        If Swimlane version is less than provided version, return -1
        
        e.g. with Swimlane version = 2.13.2-173414
            _compare_version(2) = 0
            _compare_version(1) = 1
            _compare_version(3) = -1
            
            _compare_version(2, 13) = 0
            _compare_version(2, 12) = 1
            _compare_version(2, 14) = -1
            
            _compare_version(2, 13, 3) = -1
            
            _compare_version(2, 13, 2, 173415) = -1
        """
        sections_provided = len(version_sections)

        versions = tuple(re.findall(r'\d+', self.version)[0:sections_provided])

        return (versions > version_sections) - (versions < version_sections)


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
