"""Abstractions for Swimlane app field types to simplify getting/setting values on records"""
import numbers
import weakref
from datetime import datetime

import pendulum
import six

from swimlane.core.resources.attachment import Attachment
from swimlane.core.resources.usergroup import UserGroup
from swimlane.utils import get_recursive_subclasses


# Base classes

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
        self.allow_null = allow_null
        self._value = self.default

        self.field_definition = self.record._app.get_field_definition(self.name)
        self.id = self.field_definition['id']

    def __repr__(self):
        return '<{class_name}: {py!r}>'.format(class_name=self.__class__.__name__, py=self.get_python())

    def _get(self):
        """Default getter used for both representations unless overridden"""
        return self._value

    def get_python(self):
        """Return best python representation of field value"""
        return self._get()

    def get_swimlane(self):
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
        self._value = value

    def set_python(self, value):
        """Set field internal value from the python representation of field value"""
        return self._set(value)

    def set_swimlane(self, value):
        """Set field internal value from the swimlane representation of field value"""
        return self._set(value)

    def unset(self):
        """Marks field as having no particular value"""
        self._value = self.default


class ReadOnly(object):
    """Mixin disabling setting value via python"""

    def set_python(self, value):
        raise ValueError('Cannot manually set field "{}"'.format(self.name))


# Concrete Fields

class TextField(Field):

    _field_type = 'Core.Models.Fields.TextField, Core'

    supported_types = six.string_types

    def _set(self, value):
        if value is not None and not isinstance(value, self.supported_types):
            value = str(value)

        return super(TextField, self)._set(value)


class TrackingField(ReadOnly, TextField):

    _field_type = 'Core.Models.Fields.TrackingField, Core'


class ValuesListField(TextField):

    _field_type = 'Core.Models.Fields.ValuesListField, Core'

    def __init__(self, *args, **kwargs):
        super(ValuesListField, self).__init__(*args, **kwargs)
        self.selection_type = self.field_definition['selectionType']
        self.selection_to_id_map = {f['name']: f['id'] for f in self.field_definition['values']}

    def _validate_value(self, value):
        super(ValuesListField, self)._validate_value(value)

        if value is not None:
            if value not in self.selection_to_id_map:
                raise ValueError('Field "{}" invalid value "{}". Valid options: {}'.format(
                    self.name,
                    value,
                    ', '.join(self.selection_to_id_map.keys())
                ))

    def set_swimlane(self, value):
        value = value['value']
        return super(ValuesListField, self).set_swimlane(value)

    def get_swimlane(self):
        value = super(ValuesListField, self).get_swimlane()
        return {
            '$type': 'Core.Models.Record.ValueSelection, Core',
            'id': self.selection_to_id_map[value],
            'value': value
        }


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

    def set_swimlane(self, value):
        if value is not None:
            value = pendulum.parse(value)

        return super(DatetimeField, self).set_swimlane(value)

    def get_swimlane(self):
        value = super(DatetimeField, self).get_swimlane()

        if value is not None:
            value = value.to_rfc3339_string()

        return value


class UserGroupField(Field):
    """Manages getting/setting users from record User/Group fields"""

    _field_type = 'Core.Models.Fields.UserGroupField, Core'

    supported_types = [UserGroup]

    def set_swimlane(self, value):
        """Convert JSON definition to UserGroup object"""
        # v2.x does not provide a distinction between users and groups at the field selection level, can only return
        # UserGroup instances instead of specific User or Group instances
        if value is not None:
            value = UserGroup(self.record._swimlane, value)

        return super(UserGroupField, self).set_swimlane(value)

    def get_swimlane(self):
        """Dump UserGroup back to JSON representation"""
        value = super(UserGroupField, self).get_swimlane()

        if value is not None:
            value = value.get_usergroup_selection()

        return value


class CommentsField(ReadOnly, Field):

    _field_type = 'Core.Models.Fields.CommentsField, Core'


class AttachmentsField(ReadOnly, Field):

    _field_type = 'Core.Models.Fields.AttachmentField, Core'

    def set_swimlane(self, value):
        if value is None:
            value = []

        value = [Attachment(self.record._swimlane, raw) for raw in value]

        return super(AttachmentsField, self).set_swimlane(value)


class ReferenceField(ReadOnly, Field):

    _field_type = 'Core.Models.Fields.Reference.ReferenceField, Core'


class HistoryField(ReadOnly, Field):

    _field_type = 'Core.Models.Fields.History.HistoryField, Core'


# Lookup corresponding field given a Swimlane "$type" key
FIELD_TYPE_MAP = {f._field_type: f for f in get_recursive_subclasses(Field) if f._field_type}


def resolve_field_class(field_definition):
    """Return field class most fitting of provided Swimlane field definition"""
    try:
        return FIELD_TYPE_MAP[field_definition['$type']]
    except KeyError:
        raise ValueError('No field available to handle Swimlane $type "{}"'.format(field_definition))
