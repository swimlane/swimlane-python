import pendulum
import datetime
import pytz

import pytest

from swimlane.exceptions import ValidationError

UTC = pendulum.timezone('UTC')

datetime_now = datetime.datetime.now(pytz.timezone('MST'))
pendulum_now = pendulum.instance(datetime_now)

pendulum_interval = pendulum.interval(minutes=5)


@pytest.mark.parametrize('field_name,dt,expected_raw', [
    ('Incident Closed', pendulum_now, UTC.convert(pendulum_now).to_rfc3339_string()),
    (
        'Date Field',
        pendulum_now,
        pendulum.Pendulum(pendulum_now.year, pendulum_now.month, pendulum_now.day).to_rfc3339_string()
    ),
    ('Time Field', pendulum_now, UTC.convert(pendulum_now).to_rfc3339_string()),
    ('Incident Duration', pendulum_interval, pendulum_interval.in_seconds() * 1000)
])
def test_raw_serialization(mock_record, field_name, dt, expected_raw):
    """Test that datetime field values are appropriately serialized to raw"""
    mock_record[field_name] = dt
    field_id = mock_record._app.get_field_definition_by_name(field_name)['id']
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
