import mock

from swimlane.core.resources.app_revision import AppRevision


def test_get(mock_swimlane, mock_revision_app, raw_app_revision_data):
    mock_response = mock.MagicMock()

    with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
        # return just one revision in response
        raw_revision = raw_app_revision_data[0]
        mock_response.json.return_value = raw_revision
        mock_response.status_code = 200

        revision = mock_revision_app.revisions.get(raw_revision['revisionNumber'])

        mock_swimlane.request.assert_called_with('get', 'app/{0}/history/{1}'.format(mock_revision_app.id,
                                                                                     raw_revision['revisionNumber']))

        assert isinstance(revision, AppRevision)
        assert revision.revision_number is raw_revision['revisionNumber']
        assert revision.status is raw_revision['status']

