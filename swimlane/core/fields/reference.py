import six

from swimlane.core.fields.base.multiselect import MultiSelectCursor, MultiSelectField
from swimlane.core.resources import Record


# TODO: Move Record instance cache to field to remove additional requests after direct field set, resetting cursor
class ReferenceCursor(MultiSelectCursor):
    """Handles retrieval of target app and records"""

    def __init__(self, *args, **kwargs):
        super(ReferenceCursor, self).__init__(*args, **kwargs)

        # Should be empty to start, added to as new records are lazily retrieved
        self._retrieved_record_ids = set([r.id for r in self._elements])

    def _evaluate(self):
        """Retrieve target App, and retrieve any not already retrieved records"""
        # Get target app if not already cached

        # Scan current list of targeted IDs and retrieve any that are missing
        for target_record_id in self._field._get():
            if target_record_id in self._retrieved_record_ids:
                continue

            record = self._field.target_app.records.get(id=target_record_id)
            self._elements.add(record)
            self._retrieved_record_ids.add(record.id)

        # Yield the now populated elements as normal
        return super(ReferenceCursor, self)._evaluate()


class ReferenceField(MultiSelectField):

    field_type = 'Core.Models.Fields.Reference.ReferenceField, Core'
    # Need to support strings for ids to support lazy retrieval in the cursor
    supported_types = (Record,) + six.string_types
    cursor_class = ReferenceCursor

    def __init__(self, *args, **kwargs):
        super(ReferenceField, self).__init__(*args, **kwargs)

        self._target_app_id = self.field_definition['targetId']
        self._target_app = None
        self.is_multiselect = True

    @property
    def target_app(self):
        """Defer target app retrieval until requested"""
        if self._target_app is None:
            self._target_app = self._swimlane.apps.get(id=self._target_app_id)

        return self._target_app

    def set_python(self, value):
        """Override to store only record ids internally"""
        # TODO: Validate records are from the correct target app
        if value is not None:
            elements = []

            for el in value:
                if isinstance(el, Record):
                    el = el.id
                elements.append(el)

            value = elements

        return super(ReferenceField, self).set_python(value)

    def cast_to_swimlane(self, value):
        if value is not None:
            if isinstance(value, Record):
                value = value.id

        return value

    def get_initial_elements(self):
        # FIXME: Should return list of just ids
        return []
