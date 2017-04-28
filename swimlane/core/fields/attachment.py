import mimetypes
from io import BytesIO

import pendulum

from swimlane.core.resources import APIResource
from .base import CursorField, FieldCursor, ReadOnly


class Attachment(APIResource):
    """Loose abstraction of Swimlane attachments from attachments fields"""

    _type = 'Core.Models.Record.Attachment, Core'

    def __init__(self, swimlane, raw):
        super(Attachment, self).__init__(swimlane, raw)

        self.file_id = self._raw['fileId']
        self.filename = self._raw['filename']
        self.upload_date = pendulum.parse(self._raw['uploadDate'])

    def __str__(self):
        return str(self.filename)

    def download(self, chunk_size=1024):
        """Download attachment. Returns a BytesIO stream ready for reading with the file contents"""
        stream = BytesIO()

        response = self._swimlane.request(
            'get',
            'attachment/download/{}'.format(self.file_id),
            stream=True
        )

        for chunk in response.iter_content(chunk_size):
            stream.write(chunk)

        stream.seek(0)

        return stream


class AttachmentCursor(FieldCursor):
    """Allows creation and iteration of attachments"""

    def add(self, filename, stream, content_type=None):
        """Upload a new attachment, and add it to current fields raw data to be persisted on save
        
        Can optionally manually set the content_type, will be guessed by provided filename extension and default to 
        application/octet-stream if it cannot be guessed
        """
        # Guess file Content-Type or default
        content_type = content_type or mimetypes.guess_type(filename)[0] or 'application/octet-stream'

        response = self._record._swimlane.request(
            'post',
            'attachment',
            files={
                'file': (filename, stream, content_type)
            },
        )

        # Returns raw attachment data as list with single element
        raw_attachment_data = response.json()[0]

        attachment = Attachment(self._record._swimlane, raw_attachment_data)
        self._elements.append(attachment)

        self._record._raw['values'].setdefault(self._field.id, [])
        self._record._raw['values'][self._field.id].append(attachment._raw)

        return attachment


class AttachmentsField(ReadOnly, CursorField):

    field_type = 'Core.Models.Fields.AttachmentField, Core'
    cursor_class = AttachmentCursor

    def get_initial_elements(self):
        raw_value = self.get_swimlane() or []

        return [Attachment(self.record._swimlane, raw) for raw in raw_value]
