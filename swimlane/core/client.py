"""Core Swimlane client class"""

import logging

import jwt
import pendulum
import requests
from pyuri import URI
from requests.compat import json
from requests.packages import urllib3
from requests.structures import CaseInsensitiveDict
from six.moves.urllib.parse import urljoin

from swimlane.core.adapters import GroupAdapter, UserAdapter, AppAdapter, HelperAdapter
from swimlane.core.cache import ResourcesCache
from swimlane.core.resolver import SwimlaneResolver
from swimlane.core.resources.usergroup import User
from swimlane.exceptions import SwimlaneHTTP400Error, InvalidSwimlaneProductVersion
from swimlane.utils.version import get_package_version, compare_versions

# Disable insecure request warnings
urllib3.disable_warnings()

logger = logging.getLogger(__name__)

# pylint: disable=invalid-name
_lib_full_version = get_package_version()
_lib_major_version, _lib_minor_version = _lib_full_version.split('.')[0:2]


class Swimlane(object):
    """Swimlane API client

    Core class used throughout library for all API requests and server interactions

    Args:
        host (str): Full RFC-1738 URL pointing to Swimlane host. Defaults will be provided for all parts
        username (str): Authentication username
        password (str): Authentication password
        verify_ssl (bool): Verify SSL (ignored on HTTP). Disable to use self-signed certificates
        default_timeout (int): Default request connect and read timeout in seconds for all requests
        verify_server_version (bool): Verify server version has same major version as client package. May require
            additional requests, set False to disable check
        resource_cache_size (int): Maximum number of each resource type to keep in memory cache. Set 0 to disable
            caching. Disabled by default

    Attributes:
        host (pyuri.URI): Full RFC-1738 URL pointing to Swimlane host
        apps (AppAdapter): :class:`~swimlane.core.adapters.app.AppAdapter` configured for current Swimlane instance
        users (UserAdapter): :class:`~swimlane.core.adapters.usergroup.UserAdapter` configured for current
            Swimlane instance
        groups (GroupAdapter): :class:`~swimlane.core.adapters.usergroup.GroupAdapter` configured for current
            Swimlane instance
        resources_cache (ResourcesCache): Cache checked by all supported adapters for current Swimlane instance

    Examples:

        ::

            # Establish connection
            swimlane = Swimlane(
                'https://192.168.1.1',
                'username',
                'password',
                verify_ssl=False
            )

            # Retrieve an app
            app = swimlane.apps.get(name='Target App')

    """

    _api_root = '/api/'

    def __init__(
            self,
            host,
            username,
            password,
            verify_ssl=True,
            default_timeout=60,
            verify_server_version=True,
            resource_cache_size=0
    ):
        self.host = URI(host)
        self.host.scheme = self.host.scheme.lower() or 'https'
        self.host.path = None

        self.resources_cache = ResourcesCache(resource_cache_size)

        self.__settings = None
        self.__user = None

        self._default_timeout = default_timeout

        self._session = requests.Session()
        self._session.verify = verify_ssl
        self._session.auth = SwimlaneAuth(
            self,
            username,
            password
        )

        self.apps = AppAdapter(self)
        self.users = UserAdapter(self)
        self.groups = GroupAdapter(self)
        self.helpers = HelperAdapter(self)

        if verify_server_version:
            self.__verify_server_version()

    def __verify_server_version(self):
        """Verify connected to supported server product version

        Notes:
            Logs warning if connecting to a newer minor server version

        Raises:
            swimlane.exceptions.InvalidServerVersion: If server major version is higher than package major version
        """
        if compare_versions('.'.join([_lib_major_version, _lib_minor_version]), self.product_version) > 0:
            logger.warning('Client version {} connecting to server with newer minor release {}.'.format(
                _lib_full_version,
                self.product_version
            ))

        if compare_versions(_lib_major_version, self.product_version) != 0:
            raise InvalidSwimlaneProductVersion(
                self,
                '{}.0'.format(_lib_major_version),
                '{}.0'.format(str(int(_lib_major_version) + 1))
            )

    def __repr__(self):
        return '<{cls}: {user} @ {host} v{version}>'.format(
            cls=self.__class__.__name__,
            user=self.user,
            host=self.host,
            version=self.version
        )

    def request(self, method, api_endpoint, **kwargs):
        """Wrapper for underlying :class:`requests.Session`

        Handles generating full API URL, session reuse and auth, request defaults, and invalid response status codes

        Used throughout library as the core underlying request/response method for all interactions with server

        Args:
            method (str): Request method (get, post, put, etc.)
            api_endpoint (str): Portion of URL matching API endpoint route as listed in platform /docs help page
            **kwargs (dict): Remaining arguments passed through to actual request call

        Notes:
            All other provided kwargs are passed to underlying :meth:`requests.Session.request()` call

        Raises:
            swimlane.exceptions.SwimlaneHTTP400Error: On 400 responses with additional context about the exception
            requests.HTTPError: Any other 4xx/5xx HTTP responses

        Returns:
            requests.Response: Successful response instances

        Examples:

            Request and parse server settings endpoint response

            >>> server_settings = swimlane.request('get', 'settings').json()
        """
        while api_endpoint.startswith('/'):
            api_endpoint = api_endpoint[1:]

        # Ensure a timeout is set
        kwargs.setdefault('timeout', self._default_timeout)

        # Manually grab and dump json data to have full control over serialization
        # Emulate default requests behavior
        json_data = kwargs.pop('json', None)
        if json_data is not None:
            headers = CaseInsensitiveDict(kwargs.get('headers', {}))
            headers.setdefault('Content-Type', 'application/json')
            kwargs['headers'] = headers

            kwargs['data'] = json.dumps(json_data, sort_keys=True, separators=(',', ':'))

        response = self._session.request(method, urljoin(str(self.host) + self._api_root, api_endpoint), **kwargs)

        # Roll 400 errors up into SwimlaneHTTP400Errors with specific Swimlane error code support
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            if error.response.status_code == 400:
                raise SwimlaneHTTP400Error(error)
            else:
                raise error

        return response

    @property
    def settings(self):
        """Retrieve and cache settings from server"""
        if not self.__settings:
            self.__settings = self.request('get', 'settings').json()
        return self.__settings

    @property
    def version(self):
        """Full Swimlane version, <product_version>+<build_version>+<build_number>"""
        return self.settings['apiVersion']

    @property
    def product_version(self):
        """Swimlane product version"""
        version_separator = '+'
        if version_separator in self.version:
            # Post product/build version separation
            return self.version.split(version_separator)[0]
        # Pre product/build version separation
        return self.version.split('-')[0]

    @property
    def build_version(self):
        """Swimlane semantic build version

        Falls back to product version in pre-2.18 releases
        """
        version_separator = '+'
        if version_separator in self.version:
            # Post product/build version separation
            return self.version.split(version_separator)[1]
        # Pre product/build version separation
        return self.product_version

    @property
    def build_number(self):
        """Swimlane build number"""
        version_separator = '+'
        if version_separator in self.version:
            # Post product/build version separation
            return self.version.split(version_separator)[2]
        # Pre product/build version separation
        return self.version.split('-')[1]

    @property
    def user(self):
        """User record instance for authenticated user"""
        return self._session.auth.user


class SwimlaneAuth(SwimlaneResolver):
    """Handles authentication for all requests"""

    _token_expiration_buffer = pendulum.Interval(minutes=5)

    def __init__(self, swimlane, username, password, verify_ssl=True):
        super(SwimlaneAuth, self).__init__(swimlane)

        self._username = username
        self._password = password
        self._verify_ssl = verify_ssl

        self.user = None
        self._login_headers = {}
        self._token_expiration = pendulum.now()

    def __call__(self, request):
        """Attach necessary headers to all requests

        Automatically reauthenticate before sending request when nearing token expiration
        """

        # Refresh token if it expires soon
        if pendulum.now() + self._token_expiration_buffer >= self._token_expiration:
            self.authenticate()

        request.headers.update(self._login_headers)

        return request

    def authenticate(self):
        """Send login request and update User instance, login headers, and token expiration"""

        # Temporarily remove auth from Swimlane session for auth request to avoid recursive loop during login request
        self._swimlane._session.auth = None
        resp = self._swimlane.request(
            'post',
            'user/login',
            json={
                'userName': self._username,
                'password': self._password
            },
        )
        self._swimlane._session.auth = self

        # Get JWT from response content
        json_content = resp.json()
        token = json_content.pop('token', None)

        # Grab token expiration
        token_data = jwt.decode(token, verify=False)
        token_expiration = pendulum.from_timestamp(token_data['exp'])

        headers = {
            'Authorization': 'Bearer {}'.format(token)
        }

        # Create User instance for authenticating user from login response data
        user = User(self._swimlane, _user_raw_from_login_content(json_content))

        self._login_headers = headers
        self.user = user
        self._token_expiration = token_expiration


def _user_raw_from_login_content(login_content):
    """Returns a User instance with appropriate raw data parsed from login response content"""
    matching_keys = [
        'displayName',
        'lastLogin',
        'active',
        'name',
        'isMe',
        'lastPasswordChangedDate',
        'passwordResetRequired',
        'groups',
        'roles',
        'email',
        'isAdmin',
        'createdDate',
        'modifiedDate',
        'createdByUser',
        'modifiedByUser',
        'userName',
        'id',
        'disabled'
    ]

    raw_data = {
        '$type': User._type,
    }

    for key in matching_keys:
        if key in login_content:
            raw_data[key] = login_content[key]

    return raw_data
