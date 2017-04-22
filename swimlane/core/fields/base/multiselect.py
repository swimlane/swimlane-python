from .field import Field
from .cursor import CursorField


class MultiSelectField(Field):
    """Base class for fields that can be multi-selection or single-selection field"""

    def __init__(self, *args, **kwargs):
        super(MultiSelectField, self).__init__(*args, **kwargs)

        selection_type = self.field_definition.get('selectionType', 'single')
        if selection_type == 'multi':
            self.is_multiselect = True
        elif selection_type == 'single':
            self.is_multiselect = False
        else:
            raise ValueError('Unknown selection type "{}"'.format(selection_type))

    def _set(self, value):
        """Expect single instance of supported_types or iterable of instances of supported_types when multi-select"""
        if self.is_multiselect:
            if not hasattr(value, '__iter__'):
                raise TypeError('Multiselect field "{}" must be set to iterable objects'.format(self.name))

            elements = []
            for el in value:
                self.validate_value(el)
                elements.append(el)

            value = elements
        else:
            self.validate_value(value)

        self._value = value

    def set_swimlane(self, value):
        if self.is_multiselect:
            value = value or []
            children = []

            for child in value:
                children.append(self.cast_to_python(child))

            return self._set(children)

        else:
            return super(MultiSelectField, self).set_swimlane(value)

    def get_swimlane(self):
        if self.is_multiselect:
            value = self._get()
            children = []

            for child in value:
                children.append(self.cast_to_swimlane(child))

            return children

        else:
            return super(MultiSelectField, self).get_swimlane()


