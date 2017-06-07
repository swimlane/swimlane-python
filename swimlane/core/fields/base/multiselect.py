from sortedcontainers import SortedSet

from .cursor import CursorField, FieldCursor


class MultiSelectCursor(FieldCursor):
    """Cursor allowing setting and unsetting values on a MultiSelectField
    
    Respects parent field's validation
    """

    def __init__(self, *args, **kwargs):
        super(MultiSelectCursor, self).__init__(*args, **kwargs)

        self._elements = SortedSet(self._elements)

    def select(self, element):
        """Add an element to the set of selected elements
        
        Proxy to internal set.add and sync field
        """
        self._field.validate_value(element)
        self._elements.add(element)
        self._sync_field()

    def deselect(self, element):
        """Remove an element from the set of selected elements
        
        Proxy to internal set.remove and sync field
        """
        self._elements.remove(element)
        self._sync_field()


class MultiSelectField(CursorField):
    """Base class for fields that can be multi-selection or single-selection field"""

    cursor_class = MultiSelectCursor

    def __init__(self, *args, **kwargs):
        super(MultiSelectField, self).__init__(*args, **kwargs)

        selection_type = self.field_definition.get('selectionType', 'single')
        self.is_multiselect = selection_type == 'multi'

    def get_python(self):
        """Only return cursor instance if configured for multiselect"""
        if self.is_multiselect:
            return super(MultiSelectField, self).get_python()

        return self._get()

    def get_swimlane(self):
        if self.is_multiselect:
            value = self._get()
            children = []

            for child in value:
                children.append(self.cast_to_swimlane(child))

            return children

        return super(MultiSelectField, self).get_swimlane()

    def _set(self, value):
        """Expect single instance of supported_types or iterable of instances of supported_types when multi-select"""
        if self.is_multiselect:
            value = value or []
            elements = []

            for element in value:
                self.validate_value(element)
                elements.append(element)

            value = elements
        else:
            self.validate_value(value)

        self._value = value
        self._cursor = None

    def set_swimlane(self, value):
        if self.is_multiselect:
            value = value or []
            children = []

            for child in value:
                children.append(self.cast_to_python(child))

            return self._set(children)

        return super(MultiSelectField, self).set_swimlane(value)
