"""Base classes used to build field abstractions"""
from .field import Field
from .cursor import CursorField, FieldCursor
from .multiselect import MultiSelectField


class ReadOnly(object):
    """Mixin disabling setting value via python"""

    def set_python(self, value):
        """Disable user updating value. Raises AttributeError to emulate @property/__slots__ behavior"""
        raise AttributeError('Cannot manually set field "{}"'.format(self.name))



