import six

from swimlane.exceptions import ValidationError
from .base import MultiSelectField


class ValuesListField(MultiSelectField):

    field_type = (
        'Core.Models.Fields.ValuesListField, Core',
        'Core.Models.Fields.ValuesList.ValuesListField, Core'
    )
    supported_types = six.string_types

    def __init__(self, *args, **kwargs):
        """Map names to IDs for use in field rehydration"""
        super(ValuesListField, self).__init__(*args, **kwargs)
        self.selection_to_id_map = {f['name']: f['id'] for f in self.field_definition['values']}

    def validate_value(self, value):
        """Validate provided value is one of the valid options"""
        super(ValuesListField, self).validate_value(value)

        if value is not None:
            if value not in self.selection_to_id_map:
                raise ValidationError(
                    self.record,
                    'Field "{}" invalid value "{}". Valid options: {}'.format(
                        self.name,
                        value,
                        ', '.join(self.selection_to_id_map.keys())
                    )
                )

    def cast_to_python(self, value):
        """Store actual value as internal representation"""
        if value is not None:
            value = value['value']

        return value

    def cast_to_swimlane(self, value):
        """Rehydrate value back as full JSON representation"""
        if value is None:
            return value

        return {
            '$type': 'Core.Models.Record.ValueSelection, Core',
            'id': self.selection_to_id_map[value],
            'value': value
        }

    def cast_to_report(self, value):
        """Report format uses only the value's id"""
        value = super(ValuesListField, self).cast_to_report(value)

        if value:
            return value['id']

    def cast_to_bulk_modify(self, value):
        """Bulk modify uses the normal Swimlane representation"""
        self.validate_value(value)
        return self.cast_to_swimlane(value)
