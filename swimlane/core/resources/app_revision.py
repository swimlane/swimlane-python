import pendulum

from swimlane.core.resources.app import App
from swimlane.core.resources.base import APIResource
from swimlane.core.resources.usergroup import UserGroup


class AppRevision(APIResource):
    """Encapsulates a single revision returned from a History lookup."""

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

    @staticmethod
    def __separator():
        """
        Separator for unique ids. Unlikely to be found in application ids. Although technically we do not currently
        validate app ids in the backend for specific characters so this sequence could be found.
        """
        return ' --- '

    @staticmethod
    def get_unique_id(app_id, revision_number):
        """Return the unique identifier for the given AppRevision."""
        return '{0}{1}{2}'.format(app_id, AppRevision.__separator(), revision_number)

    @staticmethod
    def parse_unique_id(unique_id):
        return unique_id.split(AppRevision.__separator())

    def get_cache_index_keys(self):
        """Returns cache index keys for this AppRevision."""
        return {
            'app_id_revision': self.get_unique_id(self.version.id, self.revision_number)
        }
