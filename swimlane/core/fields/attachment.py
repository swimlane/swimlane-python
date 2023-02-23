import io
import mimetypes

from swimlane.core.fields.base import MultiSelectField, FieldCursor
from swimlane.core.resources.attachment import Attachment
from swimlane.utils.str_validator import validate_str


class AttachmentCursor(FieldCursor):
    """Allows creation and iteration of attachments"""

    def add(self, filename, stream, content_type=None):
        """Upload a new attachment, and add it to current fields raw data to be persisted on save

        Can optionally manually set the content_type, will be guessed by provided filename extension and default to 
        application/octet-stream if it cannot be guessed
        """
        validate_str(filename, 'filename')
        self.validate_stream(stream, 'stream')

        # Guess file Content-Type or default
        content_type = content_type or mimetypes.guess_type(
            filename)[0] or 'application/octet-stream'
        response = self._record._swimlane.request(
            'post',
            'attachment/{appId}/{fieldId}'.format(
                appId=self._record.app.id, fieldId=self._field.id),
            files={
                'file': (filename, stream, content_type)
            },
        )

        # Returns raw attachment data as list with single element
        raw_attachment_data = response.json()[0]

        attachment = Attachment(self._record._swimlane, raw_attachment_data, self._record.id, self._field.id)
        self._elements.append(attachment)

        self._sync_field()

        return attachment


    def validate_stream(self, stream, key):
        if not isinstance(stream, io.IOBase):
            raise ValueError('{} must be a stream value.'.format(key))


class AttachmentsField(MultiSelectField):

    field_type = (
        'Core.Models.Fields.AttachmentField, Core',
        'Core.Models.Fields.Attachment.AttachmentField, Core'
    )
    cursor_class = AttachmentCursor
    supported_types = [Attachment]
    bulk_modify_support = False

    def __init__(self, *args, **kwargs):
        """Override to force-set multiselect to always True"""
        super(AttachmentsField, self).__init__(*args, **kwargs)
        self.multiselect = True

    def get_initial_elements(self):
        raw_value = self.get_swimlane() or []

        return [self.cast_to_python(raw) for raw in raw_value]

    def get_batch_representation(self):
        """Return best batch process representation of field value"""
        return self.get_swimlane()

    def _set(self, value):
        """Override setter, allow clearing cursor"""
        super(AttachmentsField, self)._set(value)
        self._cursor = None

    def cast_to_python(self, value):
        return Attachment(self._swimlane, value, self.record.id, self.id)

    def cast_to_swimlane(self, value):
        return value._raw
