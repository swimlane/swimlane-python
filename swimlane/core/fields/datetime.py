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
            if self.input_type == self._type_interval:
                # Pendulum interval
                value = pendulum.interval.instance(value)
            else:
                if self.input_type == self._type_date:
                    # Pendulum date
                    if isinstance(value, date):
                        value = pendulum.combine(value, pendulum.time(0))
                elif self.input_type == self._type_time:
                    # Pendulum time
                    if isinstance(value, time):
                        value = pendulum.combine(pendulum.date.today(), value)

                # Convert to Pendulum instance in UTC
                value = UTC.convert(pendulum.instance(value))
                # Drop nanosecond precision to match Mongo precision
                value = value.microsecond_(int(math.floor(value.microsecond / 1000) * 1000))

        return super(DatetimeField, self)._set(value)

    def cast_to_python(self, value):
        if value is not None:
            if self.input_type == self._type_interval:
                value = pendulum.interval(milliseconds=int(value))
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
        return pendulum.timezone('UTC').convert(target_datetime).strftime(cls.datetime_format)

    def cast_to_swimlane(self, value):
        """Return datetimes formatted as expected by API and timespans as millisecond epochs"""
        if value is None:
            return value

        if self.input_type == self._type_interval:
            return value.in_seconds() * 1000

        return self.format_datetime(value)
