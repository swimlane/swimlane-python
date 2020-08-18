from __future__ import absolute_import

from datetime import date, datetime, time, timedelta

import math
import pendulum

from .base import Field

UTC = pendulum.timezone('UTC')


class DatetimeField(Field):

    field_type = 'Core.Models.Fields.Date.DateField, Core'

    datetime_format = '%Y-%m-%dT%H:%M:%S.%fZ'

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

        # Determine supported_types after inspecting input subtype
        self.supported_types = self._input_type_map.get(self.input_type, [datetime])

    def _set(self, value):
        # Force to appropriate Pendulum instance for consistency
        if value is not None:
            if self.input_type != self._type_interval:
                if self.input_type == self._type_date:
                    # Pendulum date
                    if isinstance(value, date):
                        value = pendulum.DateTime.combine(value, pendulum.time(0))
                elif self.input_type == self._type_time:
                    # Pendulum time
                    if isinstance(value, time):
                        value = pendulum.DateTime.combine(pendulum.today().date(), value)

                # Convert to Pendulum instance in UTC
                value = UTC.convert(pendulum.instance(value))
                # Drop nanosecond precision to match Mongo precision
                value = value.set(microsecond=int(math.floor(value.microsecond / 1000) * 1000))

        return super(DatetimeField, self)._set(value)

    def cast_to_python(self, value):
        if value is not None:
            if self.input_type == self._type_interval:
                value = pendulum.duration(milliseconds=int(value))
            else:
                value = pendulum.parse(value)

        return value

    def get_python(self):
        """Coerce to best date type representation for the field subtype"""
        value = super(DatetimeField, self).get_python()

        if value is not None:
            # Handle subtypes with matching Pendulum types
            if self.input_type == self._type_time:
                value = value.time()
            if self.input_type == self._type_date:
                value = value.date()

        return value

    @classmethod
    def format_datetime(cls, target_datetime):
        """Format datetime as expected by Swimlane API"""
        return UTC.convert(target_datetime).strftime(cls.datetime_format)

    def cast_to_swimlane(self, value):
        """Return datetimes formatted as expected by API and timespans as millisecond epochs"""
        if value is None:
            return value

        if self.input_type == self._type_interval:
            return value.in_seconds() * 1000

        return self.format_datetime(value)

    def get_batch_representation(self):
        """Return best batch process representation of field value"""
        return self.get_swimlane()

    def for_json(self):
        """Return date ISO8601 string formats for datetime, date, and time values, milliseconds for intervals"""
        value = super(DatetimeField, self).for_json()

        # Order of instance checks matters for proper inheritance checks
        if isinstance(value, pendulum.Duration):
            return value.in_seconds() * 1000
        if isinstance(value, datetime):
            return self.format_datetime(value)
        if isinstance(value, pendulum.Time):
            return str(value)
        if isinstance(value, pendulum.Date):
            return value.to_date_string()
