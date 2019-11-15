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
        """
        record_revision_raw = self._swimlane.request('get',
                                                     'app/{0}/record/{1}/history/{2}'.format(self._app.id,
                                                                                             self.record.id,
                                                                                             revision_number)).json()
        return RecordRevision(self._app, record_revision_raw)
