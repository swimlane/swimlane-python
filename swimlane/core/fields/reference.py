import six
from sortedcontainers import SortedDict

from swimlane.core.fields.base.multiselect import MultiSelectCursor, MultiSelectField
from swimlane.core.resources import Record


# FIXME: Repr broken


# TODO: Move Record instance cache to field to remove additional requests after direct field set, resetting cursor
class ReferenceCursor(MultiSelectCursor):
    """Handles lazy retrieval of target records"""

    def __init__(self, *args, **kwargs):
        super(ReferenceCursor, self).__init__(*args, **kwargs)

        self._record_cache = SortedDict()

    def _evaluate(self):
        """Retrieve any not already retrieved records"""
        # Scan current list of targeted IDs and retrieve any that are missing
        for target_record_id in self._elements:
            if target_record_id in self._record_cache:
                continue

            record = self._field.target_app.records.get(id=target_record_id)
            self._record_cache[target_record_id] = record

        # Return only the cached records currently listed in elements
        return [self._record_cache[record_id] for record_id in self._elements]

    def select(self, element):
        """Support adding Records or IDs"""
        if isinstance(element, Record):
            element = element.id

        return super(ReferenceCursor, self).select(element)

    def deselect(self, element):
        """Support removing Records or IDs"""
        if isinstance(element, Record):
            element = element.id

        return super(ReferenceCursor, self).deselect(element)


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

            for element in value:
                if isinstance(element, Record):
                    element = element.id
                elements.append(element)

            value = elements

        return super(ReferenceField, self).set_python(value)
