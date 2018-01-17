from .base import Field, ReadOnly


class TrackingField(ReadOnly, Field):

    field_type = (
        'Core.Models.Fields.TrackingField, Core',
        'Core.Models.Fields.Tracking.TrackingField, Core'
    )
    bulk_modify_support = False
