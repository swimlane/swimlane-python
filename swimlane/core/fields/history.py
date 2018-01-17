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

        self.record = record

        self.modified_date = pendulum.parse(self._raw['modifiedDate'])
        self.revision_number = int(self._raw['revisionNumber'])
        self.status = self._raw['status']

        # UserGroupSelection, can't set as User without additional lookup
        self.user = UserGroup(self._swimlane, self._raw['userId'])

        # Avoid circular imports
        from swimlane.core.resources.record import Record
        self.version = Record(self.record.app, self._raw['version'])

    def __str__(self):
        return '{} ({})'.format(self.version, self.revision_number)


class HistoryField(ReadOnly, CursorField):

    field_type = 'Core.Models.Fields.History.HistoryField, Core'
    cursor_class = RevisionCursor
    bulk_modify_support = False
