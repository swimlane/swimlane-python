from swimlane.core.resources.record import Record
from swimlane.core.resources.revision_base import RevisionBase


class RecordRevision(RevisionBase):
    """
    Encapsulates a single revision returned from a History lookup.

    Attributes:
        app_revision_number: The app revision number this record revision was created using.

    Properties:
        app_version: Returns an App corresponding to the app_revision_number of this record revision.
        version: Returns a Record corresponding to the app_version and data contained in this record revision.
    """
    def __init__(self, app, raw):
        super(RecordRevision, self).__init__(app._swimlane, raw)

        self.__app_version = None
        self._app = app

        self.app_revision_number = self._raw_version['applicationRevision']

    @property
    def app_version(self):
        """The app revision corresponding to this record revision. Lazy loaded"""
        if not self.__app_version:
            self.__app_version = self._app.revisions.get(self.app_revision_number).version
        return self.__app_version

    @property
    def version(self):
        """The record contained in this record revision. Lazy loaded. Overridden from base class."""
        if not self._version:
            self._version = Record(self.app_version, self._raw_version)
        return self._version
