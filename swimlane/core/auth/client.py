"""This module provides a client for working with Swimlane."""

from __future__ import absolute_import

import json
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
import requests
from combomethod import combomethod
from .. import SwimlaneDict
from .user_pass_auth_provider import UserPassAuthProvider

__metaclass__ = type


class Client():
    """A client for Swimlane's REST API."""

    # The default client used for all requests.
    default = None

    @classmethod
    def set_default(cls, base_url, username, password, verify_ssl=True):
        """Initialize a client that can make REST requests to Swimlane.

        Args:
            base_url (str): The base URL for Swimlane
            username (str): A Swimlane username
            password (str): The Swimlane user's password
            verify_ssl (bool): Whether or not to verify SSL certs when calling
                Swimlane (default is True).

        Returns:
            Client: An instance of a Client
        """
        cls.default = Client(base_url, username, password, verify_ssl)
        cls.default.connect()

    @classmethod
    def check_default_is_set(cls):
        """Check to see if Client.default has been set."""
        if not cls.default:
            raise Exception("There is no default client set. Call set_default "
                            "to establish a default client.")

    def __init__(self, base_url, username, password, verify_ssl=True):
        """Initialize a client that can make REST requests to Swimlane.

        Args:
            base_url (str): The base URL for Swimlane
            username (str): A Swimlane username
            password (str): The Swimlane user's password
            verify_ssl (bool): Whether or not to verify SSL certs when calling
                Swimlane (default is True).

        Returns:
            Client: An instance of a Client
        """
        self.headers = {}
        self.username = username
        self.verify_ssl = verify_ssl
        self.base_url = urljoin(base_url, "api/")
        self.provider = UserPassAuthProvider(self.base_url, username, password,
                                             self.verify_ssl)

    def connect(self):
        """Connect to the Swimlane server."""
        self.headers.update(self.provider.auth_header())

    @combomethod
    def get(self, url):
        """Get resource JSON as a dict.

        Args:
            url (str): The resource URL fragment.

        Returns
            dict: The resource JSON as a SwimlaneDict.
        """
        if self is Client:
            cls = self
            cls.check_default_is_set()
            return cls.default.get(url)

        full_url = urljoin(self.base_url, url)
        resp = requests.get(full_url, headers=self.headers,
                            verify=self.verify_ssl)
        resp.raise_for_status()
        return self.build_payload(resp)

    @combomethod
    def post(self, resource, url):
        """Post a resource to Swimlane.

        Args:
            resource (Resource): The resource.
            url (str): The url to POST to.

        Returns:
            OrderedDict: The response JSON as a SwimlaneDict.
        """
        if self is Client:
            cls = self
            cls.check_default_is_set()
            return cls.default.post(resource, url)

        return self.send_data(resource, url, requests.post)

    @combomethod
    def put(self, resource, url):
        """Put a resource to Swimlane.

        Args:
            resource (Resource): The resource.
            url (str): The url to PUT to.

        Returns:
            OrderedDict: The response JSON as a SwimlaneDict.
        """
        if self is Client:
            cls = self
            cls.check_default_is_set()
            return cls.default.put(resource, url)

        return self.send_data(resource, url, requests.put)

    def send_data(self, resource, url, func):
        """Send data to Swimlane.

        Args:
            resource (Resource): The resource.
            url (str): The url.
            func (callable): The requests function to use to send the data.

        Returns:
            dict: The response JSON as a SwimlaneDict.
        """
        full_url = urljoin(self.base_url, url)
        self.headers.update({"content-type": "application/json"})
        data = resource._fields if hasattr(resource, "_fields") else resource
        resp = func(full_url, data=json.dumps(data), headers=self.headers,
                    verify=self.verify_ssl)
        resp.raise_for_status()
        return self.build_payload(resp)

    def build_payload(self, resp):
        """Build a SwimlaneDict or a list of SwimlaneDicts from the response.

        Args:
            resp (requests.Response): The response.
        """
        if not resp.content:
            return None
        payload = resp.json()
        if isinstance(payload, list):
            return (SwimlaneDict(item) for item in payload)
        if isinstance(payload, dict):
            return SwimlaneDict(payload)
        return payload
