import numbers

from .base import Field


class NumberField(Field):

    field_type = 'Core.Models.Fields.NumericField, Core'

    supported_types = [numbers.Number]
