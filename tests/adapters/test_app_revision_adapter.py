import math

import mock

from swimlane.core.resources.app_revision import AppRevision


class TestAppRevisionAdapter(object):
    def test_get_all(self, mock_swimlane, mock_revision_app, raw_app_revision_data):
        mock_response = mock.MagicMock()
        raw_revision = raw_app_revision_data
        mock_response.json.return_value = raw_revision
        mock_response.status_code = 200

        with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
            revisions = mock_revision_app.revisions.get_all()

            mock_swimlane.request.assert_called_with('get', 'app/{0}/history'.format(mock_revision_app.id,))

            for idx, revision in enumerate(revisions):
                assert isinstance(revision, AppRevision)
                assert revision.revision_number is raw_app_revision_data[idx]['revisionNumber']

    def test_get(self, mock_swimlane, mock_revision_app, raw_app_revision_data):
        mock_response = mock.MagicMock()
        raw_revision = raw_app_revision_data[0]
        mock_response.json.return_value = raw_revision
        mock_response.status_code = 200

        with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
            revision_as_int = math.floor(raw_revision['revisionNumber']);

            revision = mock_revision_app.revisions.get(revision_as_int)

            mock_swimlane.request.assert_called_with('get', 'app/{0}/history/{1}'.format(mock_revision_app.id,
                                                                                         revision_as_int))

            assert isinstance(revision, AppRevision)
            assert revision.revision_number is raw_revision['revisionNumber']

