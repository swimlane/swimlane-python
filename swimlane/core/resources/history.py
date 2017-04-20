import pendulum

from swimlane.core.resources import APIResource
from swimlane.core.resources.usergroup import UserGroup


class History(APIResource):
    """An iterable object that automatically retrieves and caches history data for a record from API"""

    def __init__(self, record):
        super(History, self).__init__(record._swimlane, {})
        self._record = record
        self.__revisions = []
        self.__retrieved = False

    def __str__(self):
        return str(self._record)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other._record.id == self._record.id

    def __len__(self):
        return len(self.revisions)

    def __iter__(self):
        """Iterate and cache across paginated record history results"""
        for revision in self.revisions:
            yield revision

    @property
    def revisions(self):
        """Retrieves, caches, and returns the list of record revisions"""
        if not self.__retrieved:
            self.__revisions = self._retrieve_revisions()
            self.__retrieved = True

        return self.__revisions

    def _retrieve_revisions(self):
        """Retrieve and populate Revision instances from history API endpoint"""
        response = self._record._swimlane.request(
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
        self.version = Record(self.record._app, self._raw['version'])

    def __str__(self):
        return '{} ({})'.format(self.version, self.revision_number)
