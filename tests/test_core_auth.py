import pytest
import requests
from swimlane.core import auth
from swimlane.core.resources.app import App

def test_default_client():
    with pytest.raises(Exception):
        App.all()

def test_user_pass_auth():
    client = auth.Client("http://windows.local/swimlane/", "admin", "admin123")
    client.connect()
    assert len(client.headers) == 1


def test_user_pass_auth_wrong_creds():
    with pytest.raises(requests.HTTPError):
        client = auth.Client("http://windows.local/swimlane/", "a", "b")
        client.connect()
