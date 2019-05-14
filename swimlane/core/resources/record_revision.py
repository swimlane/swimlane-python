import pendulum

from swimlane.core.resources.base import APIResource
from swimlane.core.resources.usergroup import UserGroup


class RecordRevision(APIResource):
    """
    Encapsulates a single revision returned from a History lookup.
    """

    def __init__(self, app, raw):
        super(RecordRevision, self).__init__(app._swimlane, raw)
        self.__app_version = None
        self.__version = None

        self._app = app

        self.app_revision_number = self._raw['version']['applicationRevision']
        self.modified_date = pendulum.parse(self._raw['modifiedDate'])
        self.revision_number = self._raw['revisionNumber']
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
    def app_version(self):
        """The app revision corresponding to this record revision. Lazy loaded"""
        if not self.__app_version:
            self.__app_version = self._app.revisions.get(self.app_revision_number).version
        return self.__app_version

    @property
    def version(self):
        """The record contained in this record revision. Lazy loaded"""
        if not self.__version:
            # avoid circular imports
            from swimlane.core.resources.record import Record
            self.__version = Record(self.app_version, self._raw['version'])
        return self.__version
