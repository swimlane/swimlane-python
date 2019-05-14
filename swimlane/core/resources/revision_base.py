import pendulum

from swimlane.core.resources.base import APIResource
from swimlane.core.resources.usergroup import UserGroup


class Revision(APIResource):
    """
    The base class representing a single revision returned from a History lookup.

    Attributes:
        Attributes:
        modified_date: The date this app revision was created.
        revision_number: The revision number of this app revision.
        status: Indicates whether this revision is the current revision or a historical revision.
        user: The user that saved this revision of the record.
    """

    def __init__(self, swimlane, raw):
        super(Revision, self).__init__(swimlane, raw)

        self.modified_date = pendulum.parse(self._raw['modifiedDate'])
        self.revision_number = self._raw['revisionNumber']
        self.status = self._raw['status']

        # UserGroupSelection, can't set as User without additional lookup
        self.user = UserGroup(self._swimlane, self._raw['userId'])

        self._version = self._raw['version']

    def __str__(self):
        return '{} ({})'.format(self.version, self.revision_number)

    def for_json(self):
        """Return revision metadata"""
        return {
            'modifiedDate': self._raw['modifiedDate'],
            'revisionNumber': self.revision_number,
            'user': self.user.for_json()
        }
