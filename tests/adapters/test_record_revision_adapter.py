

import mock

from swimlane.core.resources.record_revision import RecordRevision
from swimlane.core.resources.usergroup import UserGroup


def test_get(mock_swimlane, mock_revision_record, raw_record_revision_data):
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = raw_record_revision_data

    with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
        revisions = mock_revision_record.revisions.get()

        mock_swimlane.request.assert_called_with('get', 'app/{0}/record/{1}/history'.format(mock_revision_record.app.id,
                                                                                            mock_revision_record.id))

        for idx, revision in enumerate(revisions):
            assert isinstance(revision, RecordRevision)
            assert revision.revision_number is raw_record_revision_data[idx]['revisionNumber']
            assert revision.status is raw_record_revision_data[idx]['status']
