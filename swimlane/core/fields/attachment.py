import mimetypes

from swimlane.core.resources.attachment import Attachment
from swimlane.exceptions import ValidationError
from .base import CursorField, FieldCursor


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


class AttachmentsField(CursorField):

    field_type = (
        'Core.Models.Fields.AttachmentField, Core',
        'Core.Models.Fields.Attachment.AttachmentField, Core'
    )
    cursor_class = AttachmentCursor

    def get_initial_elements(self):
        raw_value = self.get_swimlane() or []

        return [Attachment(self.record._swimlane, raw) for raw in raw_value]

    def _set(self, value):
        """Override setter, allow clearing cursor"""
        self.validate_value(value)
        self._value = value
        self._cursor = None

    def set_python(self, value):
        """Override to set key to None"""
        if value is None:
            value = []
            super(AttachmentsField, self).set_python(value)
        else:
            raise ValidationError(
                self.record,
                'Value can only be set to None, to add attachments use AttachmentCursor.add()'
            )
