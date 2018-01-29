import six

from .base import Field


class TextField(Field):

    field_type = (
        'Core.Models.Fields.TextField, Core',
        'Core.Models.Fields.Text.TextField, Core'
    )

    supported_types = six.string_types

    def set_python(self, value):
        """Set field internal value from the python representation of field value"""
        
        # hook exists to stringify before validation

        # set to string if not string or unicode
        if value is not None and not isinstance(value, self.supported_types) or isinstance(value, int):
            value = str(value)
        return super(TextField, self).set_python(value)

