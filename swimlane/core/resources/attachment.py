from io import BytesIO

import pendulum

from swimlane.core.resources.base import APIResource


class Attachment(APIResource):
    """Abstraction of an attachment from an AttachmentsField

    Attributes:
        file_id (str): Full file ID used in download request URL
        filename (str): Attachment filename
        upload_date (pendulum.DateTime): Pendulum datetime when attachment was uploaded
        record_id (str): Associated record ID used in download request URL
        field_id (str): Assocated field ID used in download request URL
    """

    _type = 'Core.Models.Record.Attachment, Core'

    def __init__(self, swimlane, raw, record_id, field_id):
        super(Attachment, self).__init__(swimlane, raw)

        self.file_id = self._raw['fileId']
        self.filename = self._raw['filename']
        self.upload_date = pendulum.parse(self._raw['uploadDate'])
        self.record_id = record_id
        self.field_id = field_id

    def __str__(self):
        return str(self.filename)

    def __hash__(self):
        return hash(self.file_id)

    def download(self, chunk_size=1024):
        """Download attachment

        Args:
            chunk_size (int): Byte-size of chunked download request stream

        Returns:
            BytesIO: Stream ready for reading containing the attachment file contents
        """
        stream = BytesIO()

        response = self._swimlane.request(
            'get',
            'attachment/{}/{}/{}'.format(self.record_id, self.field_id, self.file_id),
            stream=True
        )

        for chunk in response.iter_content(chunk_size):
            stream.write(chunk)

        stream.seek(0)

        return stream

    def for_json(self):
        """Return metadata for JSON-compatible representation"""
        return_value = self._raw.copy()
        return_value.pop('$type')
        return return_value
