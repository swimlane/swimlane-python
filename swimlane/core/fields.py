"""Abstractions for Swimlane app field types to simplify getting/setting values on records"""
import weakref
import numbers
from datetime import datetime

import pendulum


class Field(object):
    """Base class for abstracting Swimlane complex types"""

    _field_type = None
    _resource_type = None

    # Sentinel representing a field that has no current value
    _unset = object()

    # List of supported types, leave blank to disable type validation
    supported_types = []

    def __init__(self, name, record, default_value=_unset, allow_null=True):
        self.name = name
        self.record = weakref.proxy(record)
        self.default = default_value
        self.value = self.default
        self.allow_null = allow_null

    def __repr__(self):
        return '<{self.__class__.__name__}: {self.value}>'.format(self=self)

    def _get(self):
        """Default getter used for both representations unless overridden"""
        return self.value

    def as_python(self):
        """Return best python representation of field value"""
        return self._get()

    def as_swimlane(self):
        """Return best swimlane representation of field value"""
        return self._get()

    def _validate_value(self, value):
        """Validate value is an acceptable type"""
        if value is None:
            if not self.allow_null:
                raise ValueError('Field "{}" does not allow null and cannot be set to None')
        else:
            if self.supported_types and not isinstance(value, tuple(self.supported_types)):
                raise TypeError('Field "{}" expects one of "{}", got "{}" instead'.format(
                    self.name,
                    ', '.join([t.__name__ for t in self.supported_types]),
                    type(value).__name__)
                )

    def _set(self, value):
        """Default setter used for both representations unless overridden"""
        self._validate_value(value)

        self.value = value

    def set_from_python(self, value):
        """Set field internal value from the python representation of field value"""
        return self._set(value)

    def set_from_swimlane(self, value):
        """Set field internal value from the swimlane representation of field value"""
        return self._set(value)

    def unset(self):
        """Marks field as having no particular value"""
        self.value = self.default


class TextField(Field):

    _field_type = 'Core.Models.Fields.TextField, Core'


class TrackingField(TextField):

    _field_type = 'Core.Models.Fields.TrackingField, Core'

    def _set(self, value):
        if self.value is not self.default:
            raise ValueError('Cannot manually set tracking ID')

        return super(TrackingField, self)._set(value)


class NumberField(Field):

    _field_type = 'Core.Models.Fields.NumericField, Core'

    supported_types = [numbers.Number]


class DatetimeField(Field):

    _field_type = 'Core.Models.Fields.Date.DateField, Core'

    supported_types = [datetime]

    def _set(self, value):
        self._validate_value(value)

        # Force to Pendulum instance for consistency
        if value is not None:
            value = pendulum.instance(value)

        return super(DatetimeField, self)._set(value)

    def set_from_swimlane(self, value):
        if value is not None:
            value = pendulum.parse(value)

        return super(DatetimeField, self).set_from_swimlane(value)

    def as_swimlane(self):
        value = super(DatetimeField, self).as_swimlane()

        if value is not None:
            value = value.to_rfc3339_string()

        return value


class CommentsField(Field):

    _field_type = 'Core.Models.Fields.CommentsField, Core'


class UserGroupField(Field):
    """Manages getting/setting users from record User/Group fields"""

    _field_type = 'Core.Models.Fields.UserGroupField, Core'


class AttachmentsField(Field):

    _field_type = 'Core.Models.Fields.AttachmentField, Core'


class ValuesListField(Field):

    _field_type = 'Core.Models.Fields.ValuesListField, Core'


class ReferenceField(Field):

    _field_type = 'Core.Models.Fields.Reference.ReferenceField, Core'


class HistoryField(Field):

    _field_type = 'Core.Models.Fields.History.HistoryField, Core'


# Utilities

def _recursive_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in _recursive_subclasses(s)]


# Lookup corresponding field given a Swimlane "$type" key
type_map = {f._field_type: f for f in _recursive_subclasses(Field)}


def get_field_class(field_type):
    """Return field class most fitting of provided Swimlane $type"""
    try:
        return type_map[field_type]
    except KeyError:
        raise ValueError('No field available to handle Swimlane $type "{}"'.format(field_type))
