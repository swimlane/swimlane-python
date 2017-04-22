"""Abstractions for Swimlane app field types to simplify getting/setting values on records"""
import numbers
from datetime import datetime, timedelta, date, time

import pendulum
import six

from swimlane.core.fields.base import Field, ReadOnly
from swimlane.core.fields.attachment import AttachmentsField
from swimlane.core.fields.comment import CommentsField
from swimlane.core.fields.history import HistoryField
from swimlane.core.fields.reference import ReferenceField
from swimlane.core.resources.usergroup import UserGroup
from swimlane.utils import get_recursive_subclasses


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
        if value is not None:
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

    _type_date = 'date'
    _type_time = 'time'
    _type_interval = 'timespan'

    # All others default to datetime
    _input_type_map = {
        _type_interval: [timedelta],
        _type_date: [datetime, date],
        _type_time: [datetime, time]
    }

    def __init__(self, *args, **kwargs):
        super(DatetimeField, self).__init__(*args, **kwargs)

        self.supported_types = self._input_type_map.get(self.input_type, [datetime])

    def _set(self, value):
        self._validate_value(value)

        # Force to appropriate Pendulum instance for consistency
        if value is not None:
            if self.input_type == self._type_interval:
                # Force to Pendulum interval
                value = pendulum.interval.instance(value)
            else:
                # Force to Pendulum instance
                value = pendulum.instance(value)

        return super(DatetimeField, self)._set(value)

    def set_swimlane(self, value):
        if value is not None:
            if self.input_type == self._type_interval:
                value = pendulum.interval(milliseconds=int(value))
            else:
                value = pendulum.parse(value)

        return super(DatetimeField, self).set_swimlane(value)

    def get_swimlane(self):
        value = super(DatetimeField, self).get_swimlane()

        if value is not None:
            if self.input_type == self._type_interval:
                value = int(value.total_seconds() * 1000)
            else:
                value = value.to_rfc3339_string()

        return value

    def get_python(self):
        """Coerce to best date type representation for the field subtype"""
        value = super(DatetimeField, self).get_python()

        # Handle subtypes with matching Pendulum types
        if self.input_type == self._type_time:
            value = value.time()
        if self.input_type == self._type_date:
            value = value.date()

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


# Lookup corresponding field given a Swimlane "$type" key
FIELD_TYPE_MAP = {f._field_type: f for f in get_recursive_subclasses(Field) if f._field_type}


def resolve_field_class(field_definition):
    """Return field class most fitting of provided Swimlane field definition"""
    try:
        return FIELD_TYPE_MAP[field_definition['$type']]
    except KeyError as e:
        e.message = 'No field available to handle Swimlane $type "{}"'.format(field_definition)
        raise
