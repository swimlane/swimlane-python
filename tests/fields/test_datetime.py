import math
import pendulum
import datetime
import pytz

import pytest

from swimlane.core.fields.datetime import DatetimeField
from swimlane.exceptions import ValidationError

UTC = pendulum.timezone('UTC')

datetime_now = datetime.datetime.now(pytz.timezone('MST'))
# Mongo drops portion of microsecond, field truncates automatically for consistency
datetime_now = datetime_now.replace(microsecond=int(math.floor(datetime_now.microsecond / 1000) * 1000))
pendulum_now = pendulum.instance(datetime_now)

pendulum_interval = pendulum.interval(minutes=5)


@pytest.mark.parametrize('field_name,dt,expected_raw', [
    ('Incident Closed', pendulum_now, DatetimeField.format_datetime(pendulum_now)),
    (
        'Date Field',
        pendulum_now,
        DatetimeField.format_datetime(pendulum.Pendulum(pendulum_now.year, pendulum_now.month, pendulum_now.day))
    ),
    ('Time Field', pendulum_now, DatetimeField.format_datetime(pendulum_now)),
    ('Incident Duration', pendulum_interval, pendulum_interval.in_seconds() * 1000)
])
def test_raw_serialization(mock_record, field_name, dt, expected_raw):
    """Test that datetime field values are appropriately serialized to raw"""
    mock_record[field_name] = dt
    field_id = mock_record.app.get_field_definition_by_name(field_name)['id']
    assert mock_record._raw['values'][field_id] == expected_raw


@pytest.mark.parametrize('valid_date_obj', [
    datetime_now,
    datetime_now.date(),
    pendulum_now,
    pendulum_now.date()
])
def test_date_set(mock_record, valid_date_obj):
    """Test that the date subtype can be set to a Date or Datetime"""
    mock_record['Date Field'] = valid_date_obj
    assert mock_record['Date Field'] == pendulum_now.date()


@pytest.mark.parametrize('invalid_date_obj', [
    0,
    '2017-05-15',
    '2017-05-15T00:00:00Z',
    datetime_now.time(),
    pendulum_now.time()
])
def test_date_set_invalid(mock_record, invalid_date_obj):
    """Test providing invalid data to date field"""
    with pytest.raises(ValidationError):
        mock_record['Date Field'] = invalid_date_obj


@pytest.mark.parametrize('valid_time_obj', [
    datetime_now,
    datetime_now.astimezone(pytz.UTC).time(),
    pendulum_now,
    UTC.convert(pendulum_now).time()
])
def test_time_set(mock_record, valid_time_obj):
    """Test that the time subtype can be set to a Time or Datetime"""
    mock_record['Time Field'] = valid_time_obj
    assert mock_record['Time Field'] == UTC.convert(pendulum_now).time()


@pytest.mark.parametrize('invalid_time_obj', [
    0,
    '2017-05-15',
    '2017-05-15T00:00:00Z',
    datetime_now.date(),
    pendulum_now.date()
])
def test_time_set_invalid(mock_record, invalid_time_obj):
    """Test providing invalid data to date field"""
    with pytest.raises(ValidationError):
        mock_record['Time Field'] = invalid_time_obj


def test_strip_trailing_microseconds(mock_record):
    """Test automatic removal of microseconds section during set to match values returned from API"""
    field = 'Incident Created'
    now_with_microsecond = pendulum.now().replace(microsecond=123456)
    mock_record[field] = now_with_microsecond

    assert mock_record[field] != now_with_microsecond
    assert mock_record[field].microsecond == 123000
    assert abs((mock_record[field] - now_with_microsecond).total_seconds()) < .001

    now_sans_microsecond = now_with_microsecond.replace(microsecond=0)
    mock_record[field] = now_sans_microsecond

    assert mock_record[field] == now_sans_microsecond
