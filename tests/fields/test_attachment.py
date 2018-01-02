from datetime import datetime
from io import BytesIO

import mock
import pytest
from swimlane.core.fields.attachment import AttachmentCursor
from swimlane.core.resources.attachment import Attachment
from swimlane.exceptions import ValidationError


def test_attachment_field(mock_swimlane, mock_record):
    mock_response = mock.MagicMock()

    with mock.patch.object(mock_swimlane, 'request', return_value=mock_response):
        # AttachmentsField
        # Cursor managing iteration and addition of attachments
        attachments = mock_record['PCAP Attachment']
        assert isinstance(attachments, AttachmentCursor)
        assert len(attachments) == 1

        file_contents = b'file contents'

        mock_response.iter_content.return_value.__iter__.return_value = [file_contents]

        for attachment in attachments:
            assert isinstance(attachment, Attachment)
            assert attachment.filename == str(attachment) == '5f09afe50064b2bd718e77818b565df1.pcap'
            assert attachment.file_id == '58ebb22907637a0b488b7b17'
            assert isinstance(attachment.upload_date, datetime)
            stream = attachment.download()  # Retrieve file bytes as BytesIO stream (file-like object)
            assert isinstance(stream, BytesIO)
            content = stream.read()
            assert content == file_contents

        # Upload new attachment
        # Attachment is uploaded immediately, but not associated with record (on server) until saved
        mock_response.json.return_value = [{'$type': 'Core.Models.Record.Attachment, Core',
         'fileId': '58ebb22907637a0b488b7b17',
         'filename': '5f09afe50064b2bd718e77818b565df1.pcap',
         'uploadDate': '2017-04-10T16:26:17.017Z'}]

        new_attachment = attachments.add('filename.txt', BytesIO(b'file contents in stream/handle object'))
        assert isinstance(new_attachment, Attachment)
        assert len(attachments) == 2

        # Test adding another attachment
        attachments.add('next-filename.txt', BytesIO(b'file contents in stream/handle object'))
        assert len(attachments) == 3


def test_attachment_remove(mock_record):
    field_name = 'PCAP Attachment'
    field = mock_record.get_field(field_name)
    attachments = mock_record[field_name]
    # ensure attachments are present, and record values has the expected field id for the attachments field
    assert len(attachments) > 0
    assert field.id in mock_record._raw['values']

    # ensure ValidationError on setting to value other than 'None'
    with pytest.raises(ValidationError):
        mock_record[field_name] = 'invalid'

    mock_record[field_name] = None

    # assert new cursor
    newattachments = mock_record[field_name]
    assert len(newattachments) == 0
    assert newattachments is not attachments


def test_set_attachments_validation(mock_swimlane, mock_record):
    """Verify type validation when setting an attachments field"""
    attachment = Attachment(mock_swimlane, {
        '$type': 'Core.Models.Record.Attachment, Core',
        'fileId': '1234',
        'filename': 'filename.txt',
        'uploadDate': '2017-04-10T16:26:17.017Z'
    })

    field_name = 'PCAP Attachment'
    mock_record[field_name] = [attachment]
    assert list(mock_record[field_name]) == [attachment]

    with pytest.raises(ValidationError):
        mock_record[field_name] = [1, 2, 3]

