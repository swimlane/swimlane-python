import six

from .base import Field


class TextField(Field):

    field_type = 'Core.Models.Fields.TextField, Core'

    def _set(self, value):
        if value is not None:
            value = str(value)

        return super(TextField, self)._set(value)
