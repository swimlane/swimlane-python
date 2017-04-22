from swimlane.core.fields.base import CursorField, ReadOnly, FieldCursor


class ReferenceCursor(FieldCursor):
    """Handles retrieval of target app and records"""

    def __init__(self, *args, **kwargs):
        super(ReferenceCursor, self).__init__(*args, **kwargs)

        self._target_app = None
        # Should be empty to start, added to as new records are lazily retrieved
        self._retrieved_record_ids = set([r.id for r in self._elements])

    def evaluate(self):
        """Retrieve target App, and retrieve any not already retrieved records"""
        # Get target app if not already cached
        if self._target_app is None:
            self._target_app = self._swimlane.apps.get(id=self._field._target_app_id)

        # Scan current list of targeted IDs and retrieve any that are missing
        for target_record_id in self._field._get():
            if target_record_id in self._retrieved_record_ids:
                continue

            record = self._target_app.records.get(id=target_record_id)
            self._elements.append(record)
            self._retrieved_record_ids.add(record.id)

        # Yield the now populated elements as normal
        return super(ReferenceCursor, self).evaluate()


class ReferenceField(ReadOnly, CursorField):

    field_type = 'Core.Models.Fields.Reference.ReferenceField, Core'
    cursor_class = ReferenceCursor

    def __init__(self, *args, **kwargs):
        super(ReferenceField, self).__init__(*args, **kwargs)

        self._target_app_id = self.field_definition['targetId']

    def get_initial_elements(self):
        # TODO: Override to provide initial set of elements; Requires fix to cursor evaluate
        return super(ReferenceField, self).get_initial_elements()
