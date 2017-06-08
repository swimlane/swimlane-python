import mock


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
