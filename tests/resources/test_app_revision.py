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

    def test_get_cache_index(self, mock_ar_app_revision):
        keys = mock_ar_app_revision.get_cache_index_keys()

        assert len(keys) == 1
        assert 'app_id_revision' in keys
        assert keys['app_id_revision'] == 'a34xbNOoo2P3ivyjY --- 3.0'

    def test_for_json(self, mock_ar_app_revision):
        json = mock_ar_app_revision.for_json()

        assert 'modifiedDate' in json
        assert 'revisionNumber' in json
        assert 'user' in json

    def test_str(self, mock_ar_app_revision):
        text = str(mock_ar_app_revision)

        assert text == 'Pydriver History Test (PHT) (3.0)'
