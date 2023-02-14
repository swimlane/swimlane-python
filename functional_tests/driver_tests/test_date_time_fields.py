import pytest
import pendulum
from swimlane import exceptions


@pytest.fixture(autouse=True, scope='module')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'date time fields'
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    yield
    # teardown stuff
    helpers.cleanupData()


class TestRequiredDateTimeField:
    def test_required_field(helpers):
        timeNow = pendulum.now()
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": timeNow})
        assert theRecord["Required Date & Time"].in_tz('utc').format(
            'YYYY-MM-DD HH:mm:ss') == timeNow.in_tz('utc').format('YYYY-MM-DD HH:mm:ss')

    def test_required_field_not_set(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(**{"Date & Time": pendulum.now()})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Required field "Required Date & Time" is not set' % pytest.app.acronym


class TestDateTimeField:
    def test_datetime_field_datetime(helpers):
        timeNow = pendulum.now()
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": timeNow, "Date & Time": timeNow})
        assert theRecord["Date & Time"].in_tz('utc').format(
            'YYYY-MM-DD HH:mm:ss') == timeNow.in_tz('utc').format('YYYY-MM-DD HH:mm:ss')

    def test_datetime_field_datetime_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        theRecord["Date & Time"] = pendulum.now()
        theRecord.save()

    def test_datetime_field_date(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Date & Time": pendulum.now(), "Date & Time": pendulum.now().date()})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Field \'Date & Time\' expects one of \'datetime\', got \'Date\' instead' % pytest.app.acronym

    def test_datetime_field_date_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Date & Time"] = pendulum.now().date()
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Field \'Date & Time\' expects one of \'datetime\', got \'Date\' instead' % theRecord.tracking_id

    def test_datetime_field_time(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Date & Time": pendulum.now(), "Date & Time": pendulum.now().time()})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Field \'Date & Time\' expects one of \'datetime\', got \'Time\' instead' % pytest.app.acronym

    def test_datetime_field_time_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Date & Time"] = pendulum.now().time()
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Field \'Date & Time\' expects one of \'datetime\', got \'Time\' instead' % theRecord.tracking_id


class TestDateField:
    def test_date_field_datetime(helpers):
        timeNow = pendulum.now()
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": timeNow, "Date": timeNow})
        assert theRecord["Date"] == timeNow.date()

    def test_date_field_datetime_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        theRecord["Date"] = pendulum.now()
        theRecord.save()

    def test_date_field_date(helpers):
        timeNow = pendulum.now()
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": timeNow, "Date": timeNow.date()})
        assert theRecord["Date"] == timeNow.date()

    def test_date_field_date_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        theRecord["Date"] = pendulum.now().date()
        theRecord.save()

    def test_date_field_string(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Date & Time": pendulum.now(), "Date": pendulum.now().to_date_string()})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Field \'Date\' expects one of \'datetime\', \'date\', got \'str\' instead' % pytest.app.acronym

    def test_date_field_string_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Date"] = pendulum.now().to_date_string()
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Field \'Date\' expects one of \'datetime\', \'date\', got \'str\' instead' % theRecord.tracking_id

    def test_date_field_time(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Date & Time": pendulum.now(), "Date": pendulum.now().time()})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Field \'Date\' expects one of \'datetime\', \'date\', got \'Time\' instead' % pytest.app.acronym

    def test_date_field_time_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Date"] = pendulum.now().time()
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Field \'Date\' expects one of \'datetime\', \'date\', got \'Time\' instead' % theRecord.tracking_id


class TestTimeField:
    def test_time_field_time(helpers):
        timeNow = pendulum.now()
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": timeNow, "Time": timeNow.time()})
        assert theRecord["Time"].format('HH:mm:ss') == timeNow.format('HH:mm:ss')

    def test_time_field_time_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        theRecord["Time"] = pendulum.now().time()
        theRecord.save()

    def test_time_field_datetime(helpers):
        timeNow = pendulum.now('utc')
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": timeNow, "Time": timeNow})
        assert theRecord["Time"].format('HH:mm:ss') == timeNow.format('HH:mm:ss')

    def test_time_field_datetime_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        theRecord["Time"] = pendulum.now()
        theRecord.save()

    def test_time_field_date(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Date & Time": pendulum.now(), "Time": pendulum.now().date()})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Field \'Time\' expects one of \'datetime\', \'time\', got \'Date\' instead' % pytest.app.acronym

    def test_time_field_date_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Time"] = pendulum.now().date()
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Field \'Time\' expects one of \'datetime\', \'time\', got \'Date\' instead' % theRecord.tracking_id


class TestFirstCreatedField:
    def test_first_created_field_value(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        assert theRecord["First Created"] != None

    @pytest.mark.xfail(reason="SPT-6352: The First created should have been blocked from being set.")
    def test_first_created_field(helpers):
        datetimeValue = pendulum.tomorrow()
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now(), "First Created": datetimeValue})
        assert theRecord["First Created"] != datetimeValue

    @pytest.mark.xfail(reason="SPT-6352: The First created should have been blocked from being set.")
    def test_first_created_field_on_save(helpers):
        datetimeValue = pendulum.tomorrow()
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        theOriginalTimeCreated = theRecord["First Created"]
        theRecord["First Created"] = datetimeValue
        theRecord.save()
        assert theRecord["First Created"] == theOriginalTimeCreated


class TestLastUpdatedField:
    def test_last_updated_field_value(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        assert theRecord["Last Updated"] >= theRecord["First Created"]

    @pytest.mark.xfail(reason="SPT-6352: The Last updated should have been blocked from being set.")
    def test_last_updated_field(helpers):
        datetimeValue = pendulum.yesterday()
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now(), "Last Updated": datetimeValue})
        assert theRecord["Last Updated"] != datetimeValue

    @pytest.mark.xfail(reason="SPT-6352: The Last updated should have been blocked from being set.")
    def test_last_updated_field_on_save(helpers):
        datetimeValue = pendulum.yesterday()
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        theRecord["Last Updated"] = datetimeValue
        theRecord.save()
        assert theRecord["First Created"] < theRecord["Last Updated"]
        assert theRecord["Last Updated"] != datetimeValue


class TestTimespanField:
    def test_timespan_field(helpers):
        delta = pendulum.datetime(2012, 1, 1, 1, 2, 3) - \
            pendulum.datetime(2011, 12, 31, 22, 2, 3)
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now(), "Timespan": delta})
        assert theRecord["Timespan"] == delta

    def test_timespan_field_on_save(helpers):
        delta = pendulum.datetime(2012, 1, 1, 1, 2, 3) - \
            pendulum.datetime(2011, 12, 31, 22, 2, 3)
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        theRecord["Timespan"] = delta
        theRecord.save()

    def test_timespan_field_datetime(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Date & Time": pendulum.now(), "Timespan": pendulum.now()})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Field \'Timespan\' expects one of \'timedelta\', got \'DateTime\' instead' % pytest.app.acronym

    def test_timespan_field_datetime_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Timespan"] = pendulum.now()
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Field \'Timespan\' expects one of \'timedelta\', got \'DateTime\' instead' % theRecord.tracking_id

    def test_timespan_field_number(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Date & Time": pendulum.now(), "Timespan": 123})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Field \'Timespan\' expects one of \'timedelta\', got \'int\' instead' % pytest.app.acronym

    def test_timespan_field_number_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Timespan"] = 123
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Field \'Timespan\' expects one of \'timedelta\', got \'int\' instead' % theRecord.tracking_id

    def test_timespan_field_pendulum_interval(helpers):
        delta = pendulum.duration(days=15)
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now(), "Timespan": delta})
        assert theRecord["Timespan"] == delta

    def test_timespan_field_pendulum_interval_on_save(helpers):
        delta = pendulum.duration(days=30)
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        theRecord["Timespan"] = delta
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert theRecord["Timespan"] == updatedRecord["Timespan"]


class TestReadOnlyDateTimeField:
    def test_readonly_datetime(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Date & Time": pendulum.now(), "Read-only Date & Time": pendulum.now()})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Cannot set readonly field \'Read-only Date & Time\'' % pytest.app.acronym

    def test_readonly_datetime_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Read-only Date & Time"] = pendulum.now()
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Cannot set readonly field \'Read-only Date & Time\'' % theRecord.tracking_id


class TestDefaultCurrentDateTimeField:
    @pytest.mark.xfail(reason="SPT-6353: Should this have the default value?")
    def test_default_current_field_value(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        assert theRecord["Default current Date & Time"] == theRecord["First Created"]

    def test_default_current_field(helpers):
        newDateTime = pendulum.yesterday()
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now(), "Default current Date & Time": newDateTime})
        assert theRecord["Default current Date & Time"] == newDateTime

    def test_default_current_field_on_save(helpers):
        newDateTime = pendulum.yesterday()
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        theRecord["Default current Date & Time"] = newDateTime
        theRecord.save()
        assert theRecord["Default current Date & Time"] == newDateTime


class TestDefaultSpecificDateTimeField:
    def test_default_specific_field_value(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        assert theRecord["Specific Date & Time"] == pendulum.parse(
            "Apr 1, 2020 12:00 AM -06:00", strict=False)

    def test_default_specific_field(helpers):
        newDateTime = pendulum.yesterday()
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now(), "Specific Date & Time": newDateTime})
        assert theRecord["Specific Date & Time"] == newDateTime

    def test_default_specific_field_on_save(helpers):
        newDateTime = pendulum.yesterday()
        theRecord = pytest.app.records.create(
            **{"Required Date & Time": pendulum.now()})
        theRecord["Specific Date & Time"] = newDateTime
        theRecord.save()
        assert theRecord["Specific Date & Time"] == newDateTime
