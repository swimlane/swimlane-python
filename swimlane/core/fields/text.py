import six

from .base import Field


class TextField(Field):

    field_type = 'Core.Models.Fields.TextField, Core'

    supported_types = six.string_types

    def _set(self, value):
        if value is not None and not isinstance(value, self.supported_types):
            value = str(value)

        return super(TextField, self)._set(value)
