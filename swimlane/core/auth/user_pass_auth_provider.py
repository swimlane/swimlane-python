"""
This module provides a username/password-based authentication provider to be
used by Client.
"""

import requests
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


COOKIE_NAME = ".AspNet.ApplicationCookie"


class UserPassAuthProvider(object):
    """An authentication provider based on a username and password."""

    def __init__(self, base_url, username, password, verify_ssl=True):
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
        self.base_url = urljoin(base_url, "user/login")
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl

    def auth_header(self):
        """Get an auth header that can be used for HTTP requests.

        Returns:
            dict: A dict that can be converted to an HTTP request header.
        """
        creds = {"username": self.username, "password": self.password}
        resp = requests.post(self.base_url, data=creds, verify=self.verify_ssl)

        # Raise any underlying HTTPErrors if they occured
        resp.raise_for_status()

        return {"Cookie": COOKIE_NAME + "=" + resp.cookies[COOKIE_NAME]}
