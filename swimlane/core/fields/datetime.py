from __future__ import absolute_import

from datetime import date, datetime, time, timedelta

import pendulum

from .base import Field


class DatetimeField(Field):

    field_type = 'Core.Models.Fields.Date.DateField, Core'

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
        self.validate_value(value)

        # Force to appropriate Pendulum instance for consistency
        if value is not None:
            if self.input_type == self._type_interval:
                # Pendulum interval
                value = pendulum.interval.instance(value)
            elif self.input_type == self._type_date:
                # Pendulum date
                value = self._date_to_datetime(value)
            elif self.input_type == self._type_time:
                # Pendulum time
                value = self._time_to_datetime(value)
            else:
                # Pendulum instance
                value = pendulum.instance(value)

        return super(DatetimeField, self)._set(value)

    def _date_to_datetime(self, value):
        """Convert date to datetime or raise TypeError if not possible
        
        Time component is set to 00:00:00
        """
        if isinstance(value, date):
            value = pendulum.combine(value, pendulum.time(0))

        return value

    def _time_to_datetime(self, value):
        """Convert time to datetime or raise TypeError if not possible
        
        Date component is set to today
        """
        if isinstance(value, time):
            value = pendulum.combine(pendulum.date.today(), value)

        return value

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

