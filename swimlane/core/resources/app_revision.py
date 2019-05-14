import pendulum

from swimlane.core.resources.app import App
from swimlane.core.resources.base import APIResource
from swimlane.core.resources.usergroup import UserGroup


class AppRevision(APIResource):
    """
    Encapsulates a single revision returned from a History lookup.
    """

    def __init__(self, swimlane, raw):
        super(AppRevision, self).__init__(swimlane, raw)
        self.version = App(swimlane, raw['version'])

        self.modified_date = pendulum.parse(self._raw['modifiedDate'])
        self.revision_number = self._raw['revisionNumber']
        self.status = self._raw['status']

        # UserGroupSelection, can't set as User without additional lookup
        self.user = UserGroup(self._swimlane, self._raw['userId'])

    def __str__(self):
        return '{} ({})'.format(self.version, self.revision_number)
