import math

from swimlane.core.resolver import AppResolver
from swimlane.core.resources.record_revision import RecordRevision


class RecordRevisionAdapter(AppResolver):
    """Handles retrieval of Swimlane Record Revision resources"""

    def __init__(self, app, record):
        super(RecordRevisionAdapter, self).__init__(app)
        self.record = record

    def get_all(self):
        """Get all revisions for a single record.

        Returns:
            RecordRevision[]: All record revisions for the given record ID.
        """
        raw_revisions = self._swimlane.request('get',
                                               'app/{0}/record/{1}/history'.format(self._app.id, self.record.id)).json()
        return [RecordRevision(self._app, raw) for raw in raw_revisions]

    def get(self, revision_number):
        """Gets a specific record revision.

        Keyword Args:
            revision_number (float): Record revision number

        Returns:
            RecordRevision: The RecordRevision for the given revision number.
            Raises: When revision is not an integer, a float NOT ending in ".0", or is less than 1
        """
        if isinstance(revision_number, (int, float)):
            if revision_number > 0 and revision_number % math.floor(revision_number) == 0:
                record_revision_raw = self._swimlane.request('get',
                                                             'app/{0}/record/{1}/history/{2}'.format(self._app.id,
                                                                                                     self.record.id,
                                                                                                     revision_number)).json()
                return RecordRevision(self._app, record_revision_raw)


        raise ValueError('The revision number must be a positive whole number greater than 0')