import pendulum
import datetime
import pytz

import pytest

datetime_now = datetime.datetime.now(pytz.utc)
pendulum_now = pendulum.instance(datetime_now)


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
    with pytest.raises(TypeError):
        mock_record['Date Field'] = invalid_date_obj


@pytest.mark.parametrize('valid_time_obj', [
    datetime_now,
    datetime_now.time(),
    pendulum_now,
    pendulum_now.time()
])
def test_time_set(mock_record, valid_time_obj):
    """Test that the time subtype can be set to a Time or Datetime"""
    mock_record['Time Field'] = valid_time_obj
    assert mock_record['Time Field'] == pendulum_now.time()


@pytest.mark.parametrize('invalid_time_obj', [
    0,
    '2017-05-15',
    '2017-05-15T00:00:00Z',
    datetime_now.date(),
    pendulum_now.date()
])
def test_time_set_invalid(mock_record, invalid_time_obj):
    """Test providing invalid data to date field"""
    with pytest.raises(TypeError):
        mock_record['Time Field'] = invalid_time_obj
