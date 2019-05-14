import pendulum
import pytest

from swimlane.core.resources.app import App
from swimlane.core.resources.app_revision import AppRevision
from swimlane.core.resources.usergroup import UserGroup


@pytest.fixture
def mock_ar_raw_app_revision(raw_app_revision_data):
    return raw_app_revision_data[0]


@pytest.fixture
def mock_ar_app_revision(mock_swimlane, mock_ar_raw_app_revision):
    return AppRevision(mock_swimlane, mock_ar_raw_app_revision)


class TestAppRevision(object):
    def test_constructor(self, mock_swimlane, mock_ar_app_revision, mock_ar_raw_app_revision):
        assert str(mock_ar_app_revision.modified_date) == str(pendulum.parse(mock_ar_raw_app_revision['modifiedDate']))
        assert mock_ar_app_revision.revision_number is mock_ar_raw_app_revision['revisionNumber']
        assert mock_ar_app_revision.status is mock_ar_raw_app_revision['status']
        assert str(mock_ar_app_revision.user) == str(UserGroup(mock_swimlane, mock_ar_raw_app_revision['userId']))

    def test_version(self, mock_ar_app_revision):
        version = mock_ar_app_revision.version

        assert isinstance(version, App)
        assert version._raw is mock_ar_app_revision._raw['version']
