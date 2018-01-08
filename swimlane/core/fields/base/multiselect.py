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

    def get_python(self):
        """Only return cursor instance if configured for multiselect"""
        if self.multiselect:
            return super(MultiSelectField, self).get_python()

        return self._get()

    def get_swimlane(self):
        """Handle multi-select and single-select modes"""
        if self.multiselect:
            value = self._get()
            children = []
            if value:
                for child in value:
                    children.append(self.cast_to_swimlane(child))

                return children
            return None
        return super(MultiSelectField, self).get_swimlane()

    def _set(self, value):
        """Override to treat empty lists as None"""
        return super(MultiSelectField, self)._set(value or None)

    def set_python(self, value):
        """Override to remove key from raw data when empty to work with server 2.16+ validation"""
        if self.multiselect:
            value = value or []
            elements = []

            for element in value:
                self.validate_value(element)
                elements.append(element)

            value = elements
        else:
            self.validate_value(value)

        self._set(value)

    def set_swimlane(self, value):
        """Cast all multi-select elements to correct internal type like single-select mode"""
        if self.multiselect:
            value = value or []
            children = []

            for child in value:
                children.append(self.cast_to_python(child))

            return self._set(children)

        return super(MultiSelectField, self).set_swimlane(value)
