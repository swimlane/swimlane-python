import pendulum

from swimlane.core.resources import APIResource


class Attachment(APIResource):
    """Loose abstraction of Swimlane attachments from attachments fields"""

    _type = 'Core.Models.Record.Attachment, Core'

    def __init__(self, *args, **kwargs):
        super(Attachment, self).__init__(*args, **kwargs)

        self.file_id = self._raw['fileId']
        self.filename = self._raw['filename']
        self.upload_date = pendulum.parse(self._raw['uploadDate'])

    def __str__(self):
        return str(self.filename)

    def download(self):
        """Download attachment. Returns file contents as bytes"""
        raise NotImplementedError
