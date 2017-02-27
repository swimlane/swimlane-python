"""This module provides a username/password-based authentication provider to be
used by Client.
"""

import requests
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class UserPassAuthProvider(object):
    """An authentication provider based on a username and password."""

    def __init__(self, base_url, username, password, session=None):
        """Initialize a provider that can authenticate with Swimlane using
        a username and a password.

        Args:
            base_url (str): The base URL for Swimlane
            username (str): A Swimlane username
            password (str): The Swimlane user's password
            verify_ssl (bool): Whether or not to verify SSL certs when calling
                Swimlane (default is True).

        Returns:
            UserPassAuthProvider: An instance of a UserPassAuthProvider
        """
        self.session = session or requests.Session()
        self.base_url = urljoin(base_url, "user/login")
        self.username = username
        self.password = password

    def auth_header(self):
        """Get an auth header that can be used for HTTP requests.

        Returns:
            dict: A dict that contains session cookies used in every futher HTTP request.
        """
        creds = {"username": self.username, "password": self.password}
        resp = self.session.post(self.base_url, json=creds)

        # Raise any underlying HTTPErrors if they occurred
        resp.raise_for_status()

        json_content = resp.json()

        # Check for token in response content
        token = json_content.get('token')

        if token is None:
            # Legacy cookie authentication (2.13-)
            headers ={'Cookie': ';'.join(
                ["%s=%s" % cookie for cookie in resp.cookies.items()]
            )}
        else:
            # JWT auth (2.14+)
            headers = {
                'Authorization': 'Bearer {}'.format(token)
            }

        return headers

