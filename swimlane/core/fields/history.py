import pendulum

from swimlane.core.resources.base import APIResource
from swimlane.core.resources.usergroup import UserGroup
from .base import CursorField, FieldCursor, ReadOnly


class RevisionCursor(FieldCursor):
    """An iterable object that automatically lazy retrieves and caches history data for a record from API"""

    def __init__(self, *args, **kwargs):
        super(RevisionCursor, self).__init__(*args, **kwargs)
        self.__retrieved = False

    def _evaluate(self):
        """Lazily retrieves, caches, and returns the list of record _revisions"""
        if not self.__retrieved:
            self._elements = self._retrieve_revisions()
            self.__retrieved = True

        return super(RevisionCursor, self)._evaluate()

    def _retrieve_revisions(self):
        """Retrieve and populate Revision instances from history API endpoint"""
        response = self._swimlane.request(
            'get',
            'history',
            params={
                'type': 'Records',
                'id': self._record.id
            }
        )

        raw_revisions = response.json()

        return [Revision(self._record, raw) for raw in raw_revisions]


class Revision(APIResource):
    """Encapsulates a single revision returned from a History lookup"""

    def __init__(self, record, raw):
        super(Revision, self).__init__(record._swimlane, raw)
        self.__app_revision = None
        self.__version = None

        self.record = record

        self.modified_date = pendulum.parse(self._raw['modifiedDate'])
        self.revision_number = int(self._raw['revisionNumber'])
        self.status = self._raw['status']

        # UserGroupSelection, can't set as User without additional lookup
        self.user = UserGroup(self._swimlane, self._raw['userId'])

    def __str__(self):
        return '{} ({})'.format(self.version, self.revision_number)

    def for_json(self):
        """Return revision metadata"""
        return {
            'modifiedDate': self._raw['modifiedDate'],
            'revisionNumber': self.revision_number,
            'user': self.user.for_json()
        }

    @property
    def app_revision(self):
        """Deferring request for app revision until needed"""
        if not self.__app_revision:
            # Avoid circular imports
            from swimlane.core.resources.app import App

            app_revision_number = int(self._raw['version']['applicationRevision'])
            app_revision_raw = self._swimlane.request(
                'get',
                '/app/{}/history/{}'.format(
                    self.record.app.id,
                    app_revision_number)).json()
            self.__app_revision = App(self._swimlane, app_revision_raw['version'])
        return self.__app_revision

    @property
    def version(self):
        """Deferring for sake of app revision"""
        if not self.__version:
            # Avoid circular imports
            from swimlane.core.resources.record import Record

            self.__version = Record(self.app_revision, self._raw['version'])
        return self.__version

class HistoryField(ReadOnly, CursorField):

    field_type = 'Core.Models.Fields.History.HistoryField, Core'
    cursor_class = RevisionCursor
    bulk_modify_support = False
