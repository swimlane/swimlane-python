import mock

app_id = '123'
record_id = '456'
field_id = '789'


def test_add_references(mock_swimlane):
    """Test the helper add-references route"""

    app_id = '123'
    record_id = '456'
    field_id = '789'
    target_record_ids = [
        app_id,
        record_id,
        field_id
    ]

    with mock.patch.object(mock_swimlane, 'request') as mock_request:
        mock_swimlane.helpers.add_record_references(
            app_id,
            record_id,
            field_id,
            target_record_ids
        )

        mock_request.assert_called_once_with(
            'post',
            'app/{}/record/{}/add-references'.format(app_id, record_id),
            json={
                'fieldId': field_id,
                'targetRecordIds': target_record_ids
            }
        )


def test_add_comment(mock_swimlane):
    with mock.patch.object(mock_swimlane, 'request') as mock_request:
        mock_swimlane.helpers.add_comment(
            app_id,
            record_id,
            field_id,
            'message'
        )

        assert mock_request.call_count == 1

def test_check_bulk_job_status(mock_swimlane):

    job_id = 'as03235as'
    with mock.patch.object(mock_swimlane, 'request') as mock_request:
        mock_swimlane.helpers.check_bulk_job_status(job_id)
    mock_request.assert_called_once_with('get', 'logging/job/{0}'.format(job_id))