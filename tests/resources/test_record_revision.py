import mock
import pendulum
import pytest

from swimlane.core.resources.app import App
from swimlane.core.resources.record import Record
from swimlane.core.resources.record_revision import RecordRevision
from swimlane.core.resources.usergroup import UserGroup


@pytest.fixture
def mock_rr_raw_record_revision(raw_record_revision_data):
    return raw_record_revision_data[0]


@pytest.fixture
def mock_rr_app_revision(mock_app_revisions, mock_rr_raw_record_revision):
    app_revision_number = mock_rr_raw_record_revision['version']['applicationRevision']
    return next(x for x in mock_app_revisions if x.revision_number == app_revision_number)


@pytest.fixture
def mock_rr_app(mock_rr_app_revision, mock_revision_app):
    mock_revisions = mock.MagicMock()
    mock_revisions.get.return_value = mock_rr_app_revision

    mock_revisions_property = mock.PropertyMock(return_value=mock_revisions)

    # mocks App.revisions as a property so it doesn't need to be called like a method to get the mock_revisions
    # sets it up so mock_rr_app.revisions.get() returns mock_rr_app_revision
    with mock.patch.object(mock_revision_app, 'revisions', new_callable=mock_revisions_property):
        yield mock_revision_app


@pytest.fixture
def mock_rr_record_revision(mock_rr_raw_record_revision, mock_rr_app):
    return RecordRevision(mock_rr_app, mock_rr_raw_record_revision)


class TestRecordRevision(object):
    def test_constructor(self, mock_swimlane, mock_rr_record_revision, mock_rr_raw_record_revision):
        assert mock_rr_record_revision.app_revision_number is mock_rr_raw_record_revision['version'][
            'applicationRevision']
        assert str(mock_rr_record_revision.modified_date) == str(
            pendulum.parse(mock_rr_raw_record_revision['modifiedDate']))
        assert mock_rr_record_revision.revision_number is mock_rr_raw_record_revision['revisionNumber']
        assert mock_rr_record_revision.status is mock_rr_raw_record_revision['status']
        assert str(mock_rr_record_revision.user) == str(UserGroup(mock_swimlane, mock_rr_raw_record_revision['userId']))

    def test_app_version(self, mock_rr_record_revision, mock_rr_app_revision, mock_rr_app):
        app_version = mock_rr_record_revision.app_version
        mock_rr_app.revisions.get.assert_called_with(mock_rr_record_revision.app_revision_number)
        assert isinstance(app_version, App)
        assert app_version is mock_rr_app_revision.version

    def test_version(self, mock_rr_app_revision, mock_rr_record_revision):
        version = mock_rr_record_revision.version

        assert isinstance(version, Record)
        assert version.app is mock_rr_app_revision.version
        assert version._raw is mock_rr_record_revision._raw['version']

    def test_for_json(self, mock_rr_record_revision):
        json = mock_rr_record_revision.for_json()

        assert 'modifiedDate' in json
        assert 'revisionNumber' in json
        assert 'user' in json

    def test_str(self, mock_rr_record_revision):
        text = str(mock_rr_record_revision)

        assert text == 'PHT-1 (3.0)'
