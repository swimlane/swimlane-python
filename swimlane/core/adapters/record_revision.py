from swimlane.core.cache import check_cache
from swimlane.core.resolver import AppResolver
from swimlane.core.resources.record_revision import RecordRevision
from swimlane.utils import one_of_keyword_only


class RecordRevisionAdapter(AppResolver):
    """Handles retrieval and creation of Swimlane Record Revision resources"""

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
