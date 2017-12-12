import numbers

from swimlane.exceptions import ValidationError
from .base import Field


class NumberField(Field):

    field_type = (
        'Core.Models.Fields.NumericField, Core',
        'Core.Models.Fields.Numeric.NumericField, Core'
    )

    supported_types = [numbers.Number]

    def __init__(self, *args, **kwargs):
        super(NumberField, self).__init__(*args, **kwargs)

        self.min = self.field_definition.get('min')
        self.max = self.field_definition.get('max')

    def validate_value(self, value):
        super(NumberField, self).validate_value(value)

        if value is not None:
            if self.min is not None and value < self.min:
                raise ValidationError(self.record, "Field '{}' minimum value '{}', received '{}'".format(
                    self.name,
                    self.min,
                    value
                ))

            if self.max is not None and value > self.max:
                raise ValidationError(self.record, "Field '{}' maximum value '{}', received '{}'".format(
                    self.name,
                    self.max,
                    value
                ))
