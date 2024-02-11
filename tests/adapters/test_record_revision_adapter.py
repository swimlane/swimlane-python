import unittest.mock as mock

from swimlane.core.resources.record_revision import RecordRevision


class TestRecordRevisionAdapter(object):
    def test_get_all(self, mock_swimlane, mock_revision_record, raw_record_revision_data):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = raw_record_revision_data

        with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
            revisions = mock_revision_record.revisions.get_all()

            mock_swimlane.request.assert_called_with('get',
                                                     'app/{0}/record/{1}/history'.format(mock_revision_record.app.id,
                                                                                         mock_revision_record.id))

            for idx, revision in enumerate(revisions):
                assert isinstance(revision, RecordRevision)
                assert revision.revision_number is raw_record_revision_data[idx]['revisionNumber']

    def test_get(self, mock_swimlane, mock_revision_record, raw_record_revision_data):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = raw_record_revision_data[0]

        with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
            revision = mock_revision_record.revisions.get(3)

            mock_swimlane.request.assert_called_with('get', 'app/{0}/record/{1}/history/{2}'.format(
                mock_revision_record.app.id,
                mock_revision_record.id,
                3))

            assert isinstance(revision, RecordRevision)
            assert revision.revision_number is raw_record_revision_data[0]['revisionNumber']
