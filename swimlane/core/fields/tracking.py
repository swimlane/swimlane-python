from .base import Field, ReadOnly


class TrackingField(ReadOnly, Field):

    field_type = 'Core.Models.Fields.TrackingField, Core'
