import pendulum

from swimlane.core.resources.base import APIResource
from swimlane.core.resources.usergroup import UserGroup


class RevisionBase(APIResource):
    """
    The base class representing a single revision returned from a History lookup.

    Attributes:
        Attributes:
        modified_date: The date this revision was created.
        revision_number: The revision number of this revision.
        status: Indicates whether this revision is the current revision or a historical revision.
        user: The user that saved this revision.
    """

    def __init__(self, swimlane, raw):
        super(RevisionBase, self).__init__(swimlane, raw)

        self._modified_date = pendulum.parse(self._raw['modifiedDate'])
        self._revision_number = self._raw['revisionNumber']
        self.status = self._raw['status']

        # UserGroupSelection, can't set as User without additional lookup
        self._user = UserGroup(self._swimlane, self._raw['userId'])

        self._raw_version = self._raw['version']
        self._version = None

    def __str__(self):
        return '{} ({})'.format(self.version, self.revision_number)

    @property
    def version(self):
        raise NotImplementedError

    def for_json(self):
        """Return revision metadata"""
        return {
            'modifiedDate': self._raw['modifiedDate'],
            'revisionNumber': self.revision_number,
            'user': self.user.for_json()
        }
    
    @property
    def revision_number(self):
        return self._revision_number
    
    @revision_number.setter
    def revision_number(self, value):
        raise AttributeError("can't set attribute")

    @property
    def modified_date(self):
        return self._modified_date
    
    @modified_date.setter
    def modified_date(self, value):
        raise AttributeError("can't set attribute")
    
    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, value):
        raise AttributeError("can't set attribute")
