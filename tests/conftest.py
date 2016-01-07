from pytest import fixture
from swimlane.core.auth import Client


@fixture(scope="session")
def default_client():
    """Set the default client for all Swimlane requests."""
    Client.set_default("http://windows.local/swimlane/", "admin", "admin123")
