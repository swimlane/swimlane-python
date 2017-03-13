import requests
from bravado.client import SwaggerClient
from bravado.requests_client import RequestsClient
from six.moves.urllib.parse import urljoin
from pyuri import URI


class JWTAuth(object):

    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers['Authorization'] = 'Bearer {}'.format(self.token)
        return request


class Swimlane(object):
    """Swimlane API driver"""

    api_root = '/api/'
    api_swagger_path = api_root + 'swagger'

    def __init__(self, host, username, password, verify_ssl=False):
        self.host = URI(host)
        self.username = username
        self.password = password
        self._verify = verify_ssl

        self.client = self._build_swagger_client()
        self.version = self.client.settings.getAPIVersion().result()

    def _build_swagger_client(self):
        """Return Bravado Swagger client configured and authenticated for Swimlane host"""
        transport = RequestsClient()
        transport.session.verify = self._verify

        spec_url = urljoin(self.host, self.api_swagger_path)
        spec = requests.get(spec_url).json()

        # Force-set basePath to work around Swimlane reverse proxy configuration
        spec['basePath'] = self.api_root

        # Disable response validation; Our spec seems marginally broken at this point on certain required fields
        config = {
            'validate_responses': False,
            'validate_requests': False
        }

        client = SwaggerClient.from_spec(spec, http_client=transport, config=config)

        transport.session.auth = self._build_auth(client)

        return client

    def _build_auth(self, client):
        """Build transport auth for Swimlane API"""

        token = client.user.login(model={
            'userName': self.username,
            'password': self.password,
            'domain': ''
        }).result().token

        return JWTAuth(token)
