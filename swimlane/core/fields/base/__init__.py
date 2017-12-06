"""Base classes used to build field abstractions"""
from .cursor import CursorField, FieldCursor
from .field import Field
from .multiselect import MultiSelectField, MultiSelectCursor


class ReadOnly(Field):
    """Mixin explicitly disabling setting value via python"""

    def __init__(self, *args, **kwargs):
        super(ReadOnly, self).__init__(*args, **kwargs)

        self.readonly = True


