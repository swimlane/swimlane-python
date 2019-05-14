from swimlane.core.resolver import AppResolver
from swimlane.core.resources.record_revision import RecordRevision


class RecordRevisionAdapter(AppResolver):
    """Handles retrieval of Swimlane Record Revision resources"""

    def __init__(self, app, record):
        super(RecordRevisionAdapter, self).__init__(app)
        self.record = record

    def get(self):
        """Get all revisions for a single record.

        Returns:
            RecordRevision[]: All record revisions for the given record ID.
        """
        response = self._swimlane.request('get', 'app/{0}/record/{1}/history'.format(self._app.id, self.record.id))

        raw_revisions = response.json()

        return [RecordRevision(self._app, raw) for raw in raw_revisions]