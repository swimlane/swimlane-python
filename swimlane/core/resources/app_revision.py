from swimlane.core.resources.app import App
from swimlane.core.resources.revision_base import RevisionBase


class AppRevision(RevisionBase):
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

    # Separator for unique ids. Unlikely to be found in application ids. Although technically we do not currently
    # validate app ids in the backend for specific characters so this sequence could be found.
    SEPARATOR = ' --- '

    @staticmethod
    def get_unique_id(app_id, revision_number):
        """Returns the unique identifier for the given AppRevision."""
        return '{0}{1}{2}'.format(app_id, AppRevision.SEPARATOR, revision_number)

    @staticmethod
    def parse_unique_id(unique_id):
        """Returns an array containing two items: the app_id and revision number parsed from the given unique_id."""
        return unique_id.split(AppRevision.SEPARATOR)

    @property
    def version(self):
        """Returns an App from the _raw_version info in this app revision. Lazy loaded. Overridden from base class."""
        if not self._version:
            self._version = App(self._swimlane, self._raw_version)
        return self._version

    def get_cache_index_keys(self):
        """Returns cache index keys for this AppRevision."""
        return {
            'app_id_revision': self.get_unique_id(self.version.id, self.revision_number)
        }
