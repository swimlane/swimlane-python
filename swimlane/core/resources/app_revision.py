from swimlane.core.resources.app import App
from swimlane.core.resources.revision_base import Revision


class AppRevision(Revision):
    """
    Encapsulates a single revision returned from a History lookup.

    Attributes:
        Attributes:
        modified_date: The date this app revision was created.
        revision_number: The revision number of this app revision.
        status: Indicates whether this revision is the current revision or a historical revision.
        user: The user that saved this revision of the record.
        version: The App corresponding to the data contained in this app revision.
    """

    def __init__(self, swimlane, raw):
        super(AppRevision, self).__init__(swimlane, raw)

        self.version = App(swimlane, self._version)

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
