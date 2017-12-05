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


def test_attachment_remove(mock_record):
    attachments = mock_record['PCAP Attachment']
    # ensure attachments are present
    assert len(attachments) > 0

    # ensure ValidationError on setting to value other than 'None'
    with pytest.raises(ValidationError):
        mock_record['PCAP Attachment'] = 'invalid'

    mock_record['PCAP Attachment'] = None

    # ensure record is now set to empty list
    assert mock_record._raw['values']['aep2e'] == []

    # assert new cursor
    newattachments = mock_record['PCAP Attachment']
    assert len(newattachments) == 0
    assert newattachments is not attachments
