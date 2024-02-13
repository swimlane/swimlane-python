import unittest.mock as mock

import pytest
import pendulum

from swimlane.core.fields.history import RevisionCursor
from swimlane.core.resources.record_revision import RecordRevision
from swimlane.core.resources.usergroup import UserGroup
from swimlane.core.resources.app import App
from swimlane.core.resources.record import Record


@pytest.fixture
def mock_history_swimlane(mock_swimlane, raw_app_revision_data, raw_record_revision_data):
    def request_mock(method, endpoint, params=None):
        """Mocks swimlane.request function, returns the API responses for the history endpoints."""
        if 'record' in endpoint:
            return_value = raw_record_revision_data
        else:
            revision = float(endpoint.split('/')[3])
            return_value = next(x for x in raw_app_revision_data if x['revisionNumber'] == revision)

        mock_response = mock.MagicMock()
        mock_response.json.return_value = return_value
        return mock_response

    with mock.patch.object(mock_swimlane, 'request', side_effect=request_mock):
        yield mock_swimlane


@pytest.fixture
def mock_history_record(mock_history_swimlane, mock_revision_app, mock_revision_record):
    app = App(mock_history_swimlane, mock_revision_app._raw)
    return Record(app, mock_revision_record._raw)


@pytest.fixture
def history(mock_history_record):
    return mock_history_record['History']


class TestHistory(object):
    def test_revision_cursor(self, history):
        assert isinstance(history, RevisionCursor)

    def test_num_revisions(self, history):
        # Get number of revisions
        num_revisions = len(history)
        assert num_revisions == 3

    def test_revision_str(self, history):
        for revision in history:
            assert str(revision) == 'PHT-1 ({0})'.format(revision.revision_number)

    def test_revisions(self, history, mock_history_record):
        for idx, revision in enumerate(history):
            assert isinstance(revision, RecordRevision)
            assert isinstance(revision.app_version, App)
            assert isinstance(revision.modified_date, pendulum.DateTime)
            assert isinstance(revision.user, UserGroup)
            assert isinstance(revision.version, Record)
            assert revision.version.id == mock_history_record.id
            assert len(history) - revision.revision_number == idx
