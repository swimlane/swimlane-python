from io import BytesIO

import pendulum

from swimlane.core.resources import APIResource
from .base import FieldCursor, ReadOnly, CursorField


class AttachmentCursor(FieldCursor):
    """Allows creation and iteration of attachments"""


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


class AttachmentsField(ReadOnly, CursorField):

    field_type = 'Core.Models.Fields.AttachmentField, Core'
    cursor_class = AttachmentCursor

    def get_initial_elements(self):
        raw_value = self.get_swimlane() or []

        return [Attachment(self.record._swimlane, raw) for raw in raw_value]
