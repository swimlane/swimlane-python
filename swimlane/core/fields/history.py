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
        """Populate RecordRevision instances."""
        return self._record.revisions.get_all()


class HistoryField(ReadOnly, CursorField):

    field_type = 'Core.Models.Fields.History.HistoryField, Core'
    cursor_class = RevisionCursor
    bulk_modify_support = False
