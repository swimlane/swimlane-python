import pytest
from swimlane import exceptions

# create
# get
# search
# delete


@pytest.fixture(autouse=True, scope='module')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'basic app'
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.waitOnJobByID = helpers.waitOnJobByID
    pytest.py_ver_uni_str = helpers.py_ver_uni_str
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    pytest.records = []
    pytest.tempUser1 = helpers.createUser()
    pytest.tempUser2 = helpers.createUser()
    yield
    # teardown stuff
    helpers.cleanupData()


class TestRecordAdaptorCreate:
    def test_record_create_no_params(helpers):
        emptyRecord = pytest.app.records.create()
        assert emptyRecord.created == emptyRecord.modified

    def test_record_create_empty(helpers):
        emptyRecord = pytest.app.records.create(**{})
        assert emptyRecord.is_new == False
        assert emptyRecord.created == emptyRecord.modified
        pytest.records.append(emptyRecord)

    def test_record_create_with_values(helpers):
        fullRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        assert fullRecord.created == fullRecord.modified
        pytest.records.append(fullRecord)

    def test_record_create_with_some_values_set(helpers):
        textRecord = pytest.app.records.create(**{'Text': '2w3d'})
        assert textRecord.created == textRecord.modified
        pytest.records.append(textRecord)

    def test_record_create_with_some_other_values_set(helpers):
        numericRecord = pytest.app.records.create(**{'numeric': 123})
        assert numericRecord.created == numericRecord.modified
        pytest.records.append(numericRecord)

    def test_record_create_with_invalid_field_name(helpers):
        randomFieldName = 'Some Garbage'
        with pytest.raises(exceptions.UnknownField) as excinfo:
            pytest.app.records.create(**{randomFieldName: 123})
        assert str(excinfo.value) == '"<App: %s (%s)> has no field \'%s\'"' % (
            pytest.app.name, pytest.app.acronym, randomFieldName)


class TestRecordAdaptorGet:
    def test_record_get_by_id(helpers):
        recordID = pytest.records[1].id
        singleRecord = pytest.app.records.get(id=recordID)
        assert dict(singleRecord) == dict(pytest.records[1])

    @pytest.mark.xfail(reason="SPT-5947: URL is not finding the record, works in swagger")
    def test_record_get_by_tracking_id(helpers):
        recordID = pytest.records[0].tracking_id
        singleRecord = pytest.app.records.get(tracking_id=recordID)
        assert dict(singleRecord) == dict(pytest.records[0])

    def test_record_get_no_params(helpers):
        with pytest.raises(TypeError) as excinfo:
            pytest.app.records.get()
        assert str(
            excinfo.value) == 'Must provide one of id, tracking_id as keyword argument'

    def test_record_get_random_params(helpers):
        recordID = pytest.records[0].id
        with pytest.raises(TypeError) as excinfo:
            pytest.app.records.get(something=recordID)
        assert str(excinfo.value) == "Unexpected arguments: {{'something': {}}}".format(
            pytest.py_ver_uni_str(recordID))

    def test_record_get_by_random_id(helpers):
        randomID = pytest.fake.random_int()
        with pytest.raises(exceptions.HTTPError) as excinfo:
            pytest.app.records.get(id=randomID)
        assert str(excinfo.value) == 'RecordNotFound:3002: Bad Request for url: %s/api/app/%s/record/%s' % (
            pytest.swimlane_instance.host, pytest.appid, randomID)

    def test_record_get_by_empty_id(helpers):
        emptyID = ''
        with pytest.raises(ValueError) as excinfo:
            pytest.app.records.get(id=emptyID)
        assert str(excinfo.value) == 'The value provided for the key "id" cannot be empty or None'

    def test_record_get_by_null_id(helpers):
        noneID = None
        with pytest.raises(ValueError) as excinfo:
            pytest.app.records.get(id=noneID)
        assert str(excinfo.value) == 'The value provided for the key "id" cannot be empty or None'

    def test_record_get_by_random_tracking_id(helpers):
        randomID = pytest.fake.random_int()
        with pytest.raises(exceptions.HTTPError) as excinfo:
            pytest.app.records.get(tracking_id=randomID)
        assert str(excinfo.value) == 'RecordNotFound:3002: Bad Request for url: %s/api/app/%s/record/tracking/%s' % (
            pytest.swimlane_instance.host, pytest.appid, randomID)

    def test_record_get_by_empty_trackingId(helpers):
        emptyTrackingID = ''
        with pytest.raises(ValueError) as excinfo:
            pytest.app.records.get(tracking_id=emptyTrackingID)
        assert str(excinfo.value) == 'The value provided for the key "tracking_id" cannot be empty or None'

    def test_record_get_by_null_trackingId(helpers):
        noneTrackingID = None
        with pytest.raises(ValueError) as excinfo:
            pytest.app.records.get(tracking_id=noneTrackingID)
        assert str(excinfo.value) == 'The value provided for the key "tracking_id" cannot be empty or None'

class TestRecordAdaptorSearch:
    def test_record_search(helpers):
        matchingRecords = pytest.app.records.search(('Text', 'equals', None))
        assert len(matchingRecords) == 3

    def test_record_search_no_filters(helpers):
        matchingRecords = pytest.app.records.search()
        assert len(matchingRecords) == 5

    def test_record_search_invalid_operand(helpers):
        with pytest.raises(ValueError) as excinfo:
            pytest.app.records.search(('Text', 'foo', None))
        assert str(excinfo.value) == 'Operand must be one of equals, doesNotEqual, contains, excludes, lessThan, greaterThan, lessThanOrEqual, greaterThanOrEqual'

    def test_record_search_invalid_field(helpers):
        randomFieldName = 'Blah'
        with pytest.raises(exceptions.UnknownField) as excinfo:
            pytest.app.records.search((randomFieldName, 'equals', None))
        assert str(excinfo.value) == '"<App: %s (%s)> has no field \'%s\'"' % (
            pytest.app.name, pytest.app.acronym, randomFieldName)

    @pytest.mark.xfail(reason="SPT-6028: When the field and comparison values are not the same type, an error should be thrown.")
    def test_record_search_invalid_value(helpers):
        randomFieldName = 'Numeric'
        with pytest.raises(exceptions.UnknownField) as excinfo:
            pytest.app.records.search((randomFieldName, 'equals', 'Blah'))
        assert str(excinfo.value) == '"<App: %s (%s)> has no field \'%s\'"' % (
            pytest.app.name, pytest.app.acronym, randomFieldName)


class TestRecordAdaptorDelete:
    def test_record_delete(helpers):
        deleteRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': 'to be deleted'})
        trackingID = deleteRecord.tracking_id
        deleteRecord.delete()
        with pytest.raises(exceptions.HTTPError) as excinfo:
            pytest.app.records.get(tracking_id=trackingID)
        assert str(excinfo.value) == 'RecordNotFound:3002: Bad Request for url: %s/api/app/%s/record/tracking/%s' % (
            pytest.swimlane_instance.host, pytest.appid, trackingID)

    def test_record_delete_twice(helpers):
        deleteRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': 'to be deleted'})
        deleteRecord.delete()
        with pytest.raises(ValueError) as excinfo:
            deleteRecord.delete()
        assert str(excinfo.value) == 'Cannot delete a new Record'


class TestRecordAdaptorSave:
    def test_save_record_change(helpers):
        fullRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        assert fullRecord.created == fullRecord.modified
        assert len(fullRecord.revisions.get_all()) == 1
        fullRecord['numeric'] = 5
        fullRecord.save()
        assert fullRecord.created < fullRecord.modified
        assert len(fullRecord.revisions.get_all()) == 2

    def test_save_record_no_changes(helpers):
        fullRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        assert fullRecord.created == fullRecord.modified
        assert len(fullRecord.revisions.get_all()) == 1
        fullRecord.save()
        assert fullRecord.created < fullRecord.modified
        assert len(fullRecord.revisions.get_all()) == 1
