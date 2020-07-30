import pytest
import pendulum
from swimlane import exceptions
from swimlane.core.bulk import Clear, Append, Remove
# bulk_create
# bulk_delete
# bulk_modify


@pytest.fixture(autouse=True, scope='module')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'basic fields app'
    pytest.helpers = helpers
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.waitOnJobByID = helpers.waitOnJobByID
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    pytest.records = []
    pytest.tempUser1 = helpers.createUser()
    pytest.tempUser2 = helpers.createUser()
    yield
    # teardown stuff
    helpers.cleanupData()


class TestRecordAdaptorBulkCreate:
    def test_record_bulk_create_empty(helpers):
        initialEmptyRecords = len(pytest.app.records.search(
            ('Text', 'equals', None), ('Numeric', 'equals', None)))
        pytest.app.records.bulk_create({}, {}, {}, {})
        emptyRecords = pytest.app.records.search(
            ('Text', 'equals', None), ('Numeric', 'equals', None))
        assert len(emptyRecords) == 4+initialEmptyRecords

    def test_record_bulk_create_with_values(helpers):
        initalRecords = len(pytest.app.records.search(
            ('Text', 'equals', 'Happy Joy'), ('Numeric', 'equals', None)))
        pytest.app.records.bulk_create({'Text': 'Happy Joy'}, {'Text': 'Happy Joy'}, {
                                       'Text': 'Happy Joy'}, {'Text': 'Happy Joy'})
        matchingRecords = pytest.app.records.search(
            ('Text', 'equals', 'Happy Joy'), ('Numeric', 'equals', None))
        assert len(matchingRecords) == 4 + initalRecords

    def test_record_bulk_create_with_invalid_field_name(helpers):
        randomFieldName = 'Some Garbage'
        initialRecords = len(pytest.app.records.search(
            ('Text', 'equals', 'Frank did it'), ('Numeric', 'equals', None)))
        with pytest.raises(exceptions.UnknownField) as excinfo:
            pytest.app.records.bulk_create({'Text': 'Frank did it'}, {'Text': 'Frank did it'}, {
                                           'Text': 'Frank did it'}, {randomFieldName: 'Frank did it'})
        assert str(excinfo.value) == '"<App: %s (%s)> has no field \'%s\'"' % (
            pytest.app.name, pytest.app.acronym, randomFieldName)
        matchingRecords = pytest.app.records.search(
            ('Text', 'equals', 'Frank did it'), ('Numeric', 'equals', None))
        assert len(matchingRecords) == initialRecords

    def test_record_bulk_create_with_invalid_field_value(helpers):
        randomFieldName = 'Numeric'
        initialRecords = len(pytest.app.records.search(
            (randomFieldName, 'equals', 123456)))
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.bulk_create({randomFieldName: 'Frank did it'}, {
                                           randomFieldName: 123456}, {randomFieldName: 123456}, {randomFieldName: 123456})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Field \'%s\' expects one of \'Number\', got \'str\' instead' % (
            pytest.app.acronym, randomFieldName)
        emptyRecords = pytest.app.records.search(
            (randomFieldName, 'equals', 123456))
        assert len(emptyRecords) == initialRecords


class TestRecordAdaptorBulkDelete:
    def test_record_bulk_delete_list(helpers):
        emptyRecords = pytest.app.records.search(
            ('Text', 'equals', None), ('Numeric', 'equals', None))
        assert len(emptyRecords) > 0
        records = pytest.app.records.bulk_delete(*emptyRecords)
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search(
            ('Text', 'equals', None), ('Numeric', 'equals', None))) == 0

    def test_record_bulk_delete_list_no_record_matches(helpers):
        startRecordCount = len(pytest.app.records.search())
        records = pytest.app.records.bulk_delete(
            ('Text', 'equals', None), ('Numeric', 'equals', None))
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search()) == startRecordCount

    def test_record_bulk_delete_list_no_filters_or_records(helpers):
        with pytest.raises(ValueError) as excinfo:
            records = pytest.app.records.bulk_delete()
            pytest.waitOnJobByID(records)
        assert str(
            excinfo.value) == 'Must provide at least one filter tuples or Records'

    def test_record_bulk_delete_list_records_already_deleted(helpers):
        emptyRecord = pytest.app.records.create(**{})
        records = pytest.app.records.bulk_delete(emptyRecord)
        pytest.waitOnJobByID(records)

    def test_record_bulk_delete_filter(helpers):
        initalRecords = len(pytest.app.records.search(
            ('Text', 'equals', None), ('Numeric', 'equals', 234)))
        pytest.app.records.bulk_create({'Numeric': 234}, {'Numeric': 234}, {
                                       'Numeric': 234}, {'Numeric': 234})
        assert len(pytest.app.records.search(('Text', 'equals', None),
                                             ('Numeric', 'equals', 234))) == 4+initalRecords
        records = pytest.app.records.bulk_delete(
            ('Text', 'equals', None), ('Numeric', 'equals', 234))
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search(('Text', 'equals', None),
                                             ('Numeric', 'equals', 234))) == initalRecords

    def test_record_bulk_delete_filter_invalid_field(helpers):
        randomFieldName = 'Some Garbage'
        startRecordCount = len(pytest.app.records.search())
        with pytest.raises(exceptions.UnknownField) as excinfo:
            records = pytest.app.records.bulk_delete(
                (randomFieldName, 'equals', None))
            pytest.waitOnJobByID(records)
        assert str(excinfo.value) == '"<App: %s (%s)> has no field \'%s\'"' % (
            pytest.app.name, pytest.app.acronym, randomFieldName)
        assert len(pytest.app.records.search()) == startRecordCount

    @pytest.mark.xfail(reason="SPT-6028: When the field and comparison values are not the same type, an error should be thrown.")
    def test_record_bulk_delete_filter_invalid_value(helpers):
        randomFieldName = 'Numeric'
        with pytest.raises(exceptions.UnknownField) as excinfo:
            records = pytest.app.records.bulk_delete(
                (randomFieldName, 'equals', 'Hello world'))
            pytest.waitOnJobByID(records)
        assert str(excinfo.value) == '"<App: %s (%s)> has no field \'%s\'"' % (
            pytest.app.name, pytest.app.acronym, randomFieldName)

    def test_record_bulk_delete_list_twice(helpers):
        textValue = "Delete Me twice"
        pytest.app.records.bulk_create({'Text': textValue}, {'Text': textValue}, {
                                       'Text': textValue}, {'Text': textValue})

        emptyRecords = pytest.app.records.search(('Text', 'equals', textValue))
        assert len(emptyRecords) > 0
        records = pytest.app.records.bulk_delete(*emptyRecords)
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search(
            ('Text', 'equals', None), ('Numeric', 'equals', None))) == 0
        records2 = pytest.app.records.bulk_delete(*emptyRecords)
        pytest.waitOnJobByID(records2)
        logging = pytest.swimlane_instance.helpers.check_bulk_job_status(
            records2)
        recordIdsRemoved = []
        for eachRecord in emptyRecords:
            recordIdsRemoved.append('Record %s not found.' % eachRecord.id)
        for eachLog in logging:
            if (eachLog["status"] == "completed"):
                logErrors = eachLog['details']["errors"]
                for eachError in logErrors:
                    assert eachError["message"] in recordIdsRemoved
                    recordIdsRemoved.remove(eachError["message"])


class TestRecordAdaptorBulkModify:
    def test_record_bulk_modify_filter(helpers):
        inital99Records = len(pytest.app.records.search(
            ('Text', 'equals', None), ('Numeric', 'equals', 99)))
        inital989765Records = len(pytest.app.records.search(
            ('Text', 'equals', None), ('Numeric', 'equals', 98765)))
        pytest.app.records.bulk_create({'Numeric': 99}, {'Numeric': 99}, {
                                       'Numeric': 99}, {'Numeric': 99})
        records = pytest.app.records.bulk_modify(
            ('Text', 'equals', None), ('Numeric', 'equals', 99), values={'Numeric': 98765})
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search(
            ('Text', 'equals', None), ('Numeric', 'equals', 99))) == 0
        assert len(pytest.app.records.search(('Text', 'equals', None), ('Numeric',
                                                                        'equals', 98765))) == 4 + inital99Records + inital989765Records

    def test_record_bulk_modify_no_filter(helpers):
        initial99Records = len(pytest.app.records.search(
            ('Text', 'equals', None), ('Numeric', 'equals', 99)))
        initial6666Records = len(
            pytest.app.records.search(('Numeric', 'equals', 6666)))
        pytest.app.records.bulk_create({'Numeric': 99}, {'Numeric': 99}, {
                                       'Numeric': 99}, {'Numeric': 99})
        with pytest.raises(ValueError) as excinfo:
            records = pytest.app.records.bulk_modify(values={'Numeric': 6666})
            pytest.waitOnJobByID(records)
        assert str(
            excinfo.value) == 'Must provide at least one filter tuples or Records'
        assert len(pytest.app.records.search(('Text', 'equals', None),
                                             ('Numeric', 'equals', 99))) == 4 + initial99Records
        assert len(pytest.app.records.search(
            ('Numeric', 'equals', 6666))) == initial6666Records

    def test_record_bulk_modify_no_filter_matches(helpers):
        assert len(pytest.app.records.search(
            ('Text', 'equals', 'Not today'))) == 0
        initialRecords = len(pytest.app.records.search(
            ('Numeric', 'equals', 9999)))
        records = pytest.app.records.bulk_modify(
            ('Text', 'equals', 'Not today'), values={'Numeric': 9999})
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search(
            ('Numeric', 'equals', 9999))) == initialRecords

    def test_record_bulk_modify_filter_invalid_field(helpers):
        randomFieldName = 'Some Garbage'
        initialRecords = len(pytest.app.records.search(
            ('Numeric', 'equals', 9999)))
        with pytest.raises(exceptions.UnknownField) as excinfo:
            records = pytest.app.records.bulk_modify(
                (randomFieldName, 'equals', 'Not today'), values={'Numeric': 9999})
            pytest.waitOnJobByID(records)
        assert str(excinfo.value) == '"<App: %s (%s)> has no field \'%s\'"' % (
            pytest.app.name, pytest.app.acronym, randomFieldName)
        assert len(pytest.app.records.search(
            ('Numeric', 'equals', 9999))) == initialRecords

    @pytest.mark.xfail(reason="SPT-6028: When the field and comparison values are not the same type, an error should be thrown.")
    def test_record_bulk_modify_filter_invalid_value(helpers):
        randomValue = 'Fun with numbers'
        with pytest.raises(exceptions.UnknownField) as excinfo:
            records = pytest.app.records.bulk_modify(
                ('Numeric', 'equals', randomValue), values={'Numeric': 4444})
            pytest.waitOnJobByID(records)
        assert str(excinfo.value) == '"<App: %s (%s)> has no field \'%s\'"' % (
            pytest.app.name, pytest.app.acronym, randomValue)

    def test_record_bulk_modify_list(helpers):
        initial66Records = len(pytest.app.records.search(
            ('Text', 'equals', None), ('Numeric', 'equals', 66)))
        initial4321Records = len(pytest.app.records.search(
            ('Text', 'equals', None), ('Numeric', 'equals', 4321)))
        pytest.app.records.bulk_create({'Numeric': 66}, {'Numeric': 66}, {
                                       'Numeric': 66}, {'Numeric': 66})
        recordList = pytest.app.records.search(
            ('Text', 'equals', None), ('Numeric', 'equals', 66))
        records = pytest.app.records.bulk_modify(
            *recordList, values={'Numeric': 4321})
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search(('Text', 'equals', None),
                                             ('Numeric', 'equals', 66))) == initial66Records
        assert len(pytest.app.records.search(('Text', 'equals', None),
                                             ('Numeric', 'equals', 4321))) == 4 + initial4321Records

    def test_record_bulk_modify_list_records_already_deleted(helpers):
        deleteRecord = pytest.app.records.create(**{})
        copyOfDeleteRecord = pytest.app.records.get(id=deleteRecord.id)
        deleteRecord.delete()
        initialRecords = len(pytest.app.records.search(
            ('Numeric', 'equals', 77777)))
        records = pytest.app.records.bulk_modify(
            copyOfDeleteRecord, values={'Numeric': 77777})
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search(
            ('Numeric', 'equals', 77777))) == initialRecords


class TestRecordAdaptorBulkModifyClear:
    def test_record_bulk_modify_clear_numeric(helpers):
        pytest.app.records.bulk_create({'Numeric': 9999999}, {'Numeric': 9999999}, {
                                       'Numeric': 9999999}, {'Numeric': 9999999})
        initialRecords = len(pytest.app.records.search(
            ('Numeric', 'equals', 9999999)))
        emptyNumericRecords = len(
            pytest.app.records.search(('Numeric', 'equals', None)))
        records = pytest.app.records.bulk_modify(
            ('Numeric', 'equals', 9999999), values={'Numeric': Clear()})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(('Numeric', 'equals', None))
                   ) == initialRecords + emptyNumericRecords

    def test_record_bulk_modify_clear_text(helpers):
        pytest.app.records.bulk_create({'Text': '9999999'}, {'Text': '9999999'}, {
                                       'Text': '9999999'}, {'Text': '9999999'})
        initialRecords = len(pytest.app.records.search(
            ('Text', 'equals', '9999999')))
        emptyNumericRecords = len(
            pytest.app.records.search(('Text', 'equals', None)))
        records = pytest.app.records.bulk_modify(
            ('Text', 'equals', '9999999'), values={'Text': Clear()})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(('Text', 'equals', None))
                   ) == initialRecords + emptyNumericRecords

    def test_record_bulk_modify_clear_selection(helpers):
        pytest.app.records.bulk_create({'Selection': '123'}, {'Selection': '123'}, {
                                       'Selection': '123'}, {'Selection': '123'})
        initialRecords = len(pytest.app.records.search(
            ('Selection', 'equals', '123')))
        emptyNumericRecords = len(
            pytest.app.records.search(('Selection', 'equals', None)))
        records = pytest.app.records.bulk_modify(
            ('Selection', 'equals', '123'), values={'Selection': Clear()})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(
            ('Selection', 'equals', None))) == initialRecords + emptyNumericRecords

    def test_record_bulk_modify_clear_multi_selection(helpers):
        pytest.app.records.bulk_create({'Multi-select': ['one']}, {'Multi-select': ['one']}, {
                                       'Multi-select': ['one']}, {'Multi-select': ['one']})
        initialRecords = len(pytest.app.records.search(
            ('Multi-select', 'equals', ['one'])))
        emptyNumericRecords = len(pytest.app.records.search(
            ('Multi-select', 'equals', None)))
        records = pytest.app.records.bulk_modify(
            ('Multi-select', 'equals', ['one']), values={'Multi-select': Clear()})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(
            ('Multi-select', 'equals', None))) == initialRecords + emptyNumericRecords

    def test_record_bulk_modify_clear_text_list(helpers):
        pytest.app.records.bulk_create({'Text List': ['one']}, {'Text List': ['one']}, {
                                       'Text List': ['one']}, {'Text List': ['one']})
        initialRecords = len(pytest.app.records.search(
            ('Text List', 'equals', ['one'])))
        emptyNumericRecords = len(
            pytest.app.records.search(('Text List', 'equals', None)))
        records = pytest.app.records.bulk_modify(
            ('Text List', 'equals', ['one']), values={'Text List': Clear()})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(
            ('Text List', 'equals', None))) == initialRecords + emptyNumericRecords

    def test_record_bulk_modify_clear_numeric_list(helpers):
        pytest.app.records.bulk_create({'Numeric List': [12345]}, {'Numeric List': [12345]}, {
                                       'Numeric List': [12345]}, {'Numeric List': [12345]})
        initialRecords = len(pytest.app.records.search(
            ('Numeric List', 'equals', [12345])))
        emptyNumericRecords = len(pytest.app.records.search(
            ('Numeric List', 'equals', None)))
        records = pytest.app.records.bulk_modify(
            ('Numeric List', 'equals', [12345]), values={'Numeric List': Clear()})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(
            ('Numeric List', 'equals', None))) == initialRecords + emptyNumericRecords

    def test_record_bulk_modify_clear_multi_select_users(helpers):
        swimUser = pytest.swimlane_instance.users.get(
            display_name=pytest.tempUser1['displayName'])
        pytest.app.records.bulk_create({'Multi-Select Users': [swimUser]}, {'Multi-Select Users': [
                                       swimUser]}, {'Multi-Select Users': [swimUser]}, {'Multi-Select Users': [swimUser]})
        initialRecords = len(pytest.app.records.search(
            ('Multi-Select Users', 'equals', [swimUser])))
        emptyNumericRecords = len(pytest.app.records.search(
            ('Multi-Select Users', 'equals', None)))
        records = pytest.app.records.bulk_modify(
            ('Multi-Select Users', 'equals', [swimUser]), values={'Multi-Select Users': Clear()})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(('Multi-Select Users',
                                              'equals', None))) == initialRecords + emptyNumericRecords

    def test_record_bulk_modify_clear_date_time(helpers):
        baseTime = pendulum.now()
        pytest.app.records.bulk_create({'Date & Time': baseTime}, {'Date & Time': baseTime}, {
                                       'Date & Time': baseTime}, {'Date & Time': baseTime})
        initialRecords = len(pytest.app.records.search(
            ('Date & Time', 'equals', baseTime)))
        emptyNumericRecords = len(pytest.app.records.search(
            ('Date & Time', 'equals', None)))
        records = pytest.app.records.bulk_modify(
            ('Date & Time', 'equals', baseTime), values={'Date & Time': Clear()})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(
            ('Date & Time', 'equals', None))) == initialRecords + emptyNumericRecords

    def test_record_bulk_modify_clear_first_created(helpers):
        baseTime = pendulum.now()
        pytest.app.records.bulk_create({'Date & Time': baseTime}, {'Date & Time': baseTime}, {
                                       'Date & Time': baseTime}, {'Date & Time': baseTime})
        emptyNumericRecords = len(pytest.app.records.search(
            ('First Created', 'equals', None)))
        records = pytest.app.records.bulk_modify(
            ('Date & Time', 'equals', baseTime), values={'First Created': Clear()})
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search(
            ('First Created', 'equals', None))) == emptyNumericRecords

    def test_record_bulk_modify_clear_last_updated(helpers):
        baseTime = pendulum.now()
        pytest.app.records.bulk_create({'Date & Time': baseTime}, {'Date & Time': baseTime}, {
                                       'Date & Time': baseTime}, {'Date & Time': baseTime})
        emptyNumericRecords = len(pytest.app.records.search(
            ('Last Updated', 'equals', None)))
        records = pytest.app.records.bulk_modify(
            ('Date & Time', 'equals', baseTime), values={'Last Updated': Clear()})
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search(
            ('Last Updated', 'equals', None))) == emptyNumericRecords

    def test_record_bulk_modify_clear_created_by(helpers):
        baseTime = pendulum.now()
        pytest.app.records.bulk_create({'Date & Time': baseTime}, {'Date & Time': baseTime}, {
                                       'Date & Time': baseTime}, {'Date & Time': baseTime})
        emptyNumericRecords = len(
            pytest.app.records.search(('Created by', 'equals', None)))
        records = pytest.app.records.bulk_modify(
            ('Date & Time', 'equals', baseTime), values={'Created by': Clear()})
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search(
            ('Created by', 'equals', None))) == emptyNumericRecords

    def test_record_bulk_modify_clear_last_updated_by(helpers):
        baseTime = pendulum.now()
        pytest.app.records.bulk_create({'Date & Time': baseTime}, {'Date & Time': baseTime}, {
                                       'Date & Time': baseTime}, {'Date & Time': baseTime})
        emptyNumericRecords = len(pytest.app.records.search(
            ('Last updated by', 'equals', None)))
        records = pytest.app.records.bulk_modify(
            ('Date & Time', 'equals', baseTime), values={'Last updated by': Clear()})
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search(
            ('Last updated by', 'equals', None))) == emptyNumericRecords

    def test_record_bulk_modify_clear_attachment(helpers):
        baseText = "Has Attachment"
        fileName = '6.65kB.json'
        pytest.app.records.bulk_create({'Text': baseText}, {'Text': baseText}, {
                                       'Text': baseText}, {'Text': baseText})
        theFile = pytest.helpers.loadFileStream(fileName)
        for record in pytest.app.records.search(('Text', 'equals', baseText)):
            record['Attachment'].add(fileName, theFile)
            record.save()
        with pytest.raises(ValueError) as excinfo:
            pytest.app.records.bulk_modify(
                ('Text', 'equals', baseText), values={'Attachment': Clear()})
        assert str(
            excinfo.value) == 'Field \'Attachment\' of Type \'AttachmentsField\', is not supported for bulk modify'

    def test_record_bulk_modify_clear_comments(helpers):
        baseText = "Has Comment"
        pytest.app.records.bulk_create({'Text': baseText}, {'Text': baseText}, {
                                       'Text': baseText}, {'Text': baseText})
        for record in pytest.app.records.search(('Text', 'equals', baseText)):
            record['Comments'].comment(baseText)
            record.save()
        with pytest.raises(ValueError) as excinfo:
            pytest.app.records.bulk_modify(
                ('Text', 'equals', baseText), values={'Attachment': Clear()})
        assert str(
            excinfo.value) == 'Field \'Attachment\' of Type \'AttachmentsField\', is not supported for bulk modify'

    def test_record_bulk_modify_clear_references(helpers):
        baseText = "Has Reference"
        pytest.app.records.bulk_create({'Text': baseText}, {'Text': baseText}, {
                                       'Text': baseText}, {'Text': baseText})
        targetApp = pytest.swimlane_instance.apps.get(
            name="PYTHON-Helpers Target App")
        targetRecord = targetApp.records.create()

        for record in pytest.app.records.search(('Text', 'equals', baseText)):
            record['Reference'].add(targetRecord)
            record.save()
        for record in pytest.app.records.search(('Text', 'equals', baseText)):
            assert len(record['Reference']) == 1
        records = pytest.app.records.bulk_modify(
            ('Text', 'equals', baseText), values={'Reference': Clear()})
        pytest.waitOnJobByID(records)
        for record in pytest.app.records.search(('Text', 'equals', baseText)):
            assert len(record['Reference']) == 0


class TestRecordAdaptorBulkModifyAppend:
    def test_record_bulk_modify_append_text(helpers):
        pytest.app.records.bulk_create({'Text': 'hello'}, {'Text': 'hello goodbye'}, {
                                       'Text': 'goodbye'}, {'Text': 'hello goodbye fred'})
        initialRecords = len(pytest.app.records.search(
            ('Text', 'contains', 'hello')))
        alreadyHaveGlow = len(pytest.app.records.search(
            ('Text', 'contains', "glow")))
        records = pytest.app.records.bulk_modify(
            ('Text', 'contains', 'hello'), values={'Text': Append("glow")})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 3
        assert len(pytest.app.records.search(
            ('Text', 'contains', "glow"))) == initialRecords + alreadyHaveGlow

    @pytest.mark.xfail(reason="SPT-????: There was no error about the field type, nor any changes to the value")
    def test_record_bulk_modify_append_numeric(helpers):
        pytest.app.records.bulk_create({'Numeric': 123}, {'Numeric': 123}, {
                                       'Numeric': 123}, {'Numeric': 1234})
        initialRecords = len(pytest.app.records.search(
            ('Numeric', 'equals', 123)))
        records = pytest.app.records.bulk_modify(
            ('Numeric', 'equals', 123), values={'Numeric': Append(5)})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 3
        assert len(pytest.app.records.search(
            ('Numeric', 'equals', 128))) == initialRecords

    @pytest.mark.xfail(reason="SPT-????: There was no error about the field type, nor any changes to the value")
    def test_record_bulk_modify_append_selection(helpers):
        pytest.app.records.bulk_create({'Selection': 'New Value'}, {'Selection': 'New Value'}, {
                                       'Selection': 'New Value'}, {'Selection': 'New Value'})
        initialRecords = len(pytest.app.records.search(
            ('Selection', 'equals', 'New Value')))
        alreadySetRecords = len(pytest.app.records.search(
            ('Selection', 'equals', '123')))
        records = pytest.app.records.bulk_modify(
            ('Selection', 'equals', 'New Value'), values={'Selection': Append('123')})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 3
        assert len(pytest.app.records.search(
            ('Selection', 'equals', '123'))) == initialRecords + alreadySetRecords

    def test_record_bulk_modify_append_multi_selection(helpers):
        pytest.app.records.bulk_create({'Multi-select': ['one']}, {'Multi-select': ['one']}, {
                                       'Multi-select': ['one']}, {'Multi-select': ['one']})
        initialRecords = len(pytest.app.records.search(
            ('Multi-select', 'equals', ['one'])))
        records = pytest.app.records.bulk_modify(
            ('Multi-select', 'equals', ['one']), values={'Multi-select': Append(["two"])})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(
            ('Multi-select', 'contains', ["two"]))) == initialRecords

    @pytest.mark.xfail(reason="SPT-????: IS the bulk modify not working for text list???")
    def test_record_bulk_modify_append_text_list(helpers):
        pytest.app.records.bulk_create({'Text List': ['hello']}, {'Text List': ['hello', 'goodbye']}, {
                                       'Text List': ['goodbye']}, {'Text List': ['hello', 'goodbye', 'fred']})
        initialRecords = len(pytest.app.records.search(
            ('Text List', 'doesNotEqual', [])))
        records = pytest.app.records.bulk_modify(
            ('Text List', 'doesNotEqual', []), values={'Text List': Append(["glow"])})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(
            ('Text List', 'contains', "glow"))) == initialRecords

    def test_record_bulk_modify_append_numeric_list(helpers):
        pytest.app.records.bulk_create({'Numeric List': [123]}, {'Numeric List': [123, 456]}, {
                                       'Numeric List': [456]}, {'Numeric List': [123, 456, 789]})
        initialRecords = len(pytest.app.records.search(
            ('Numeric List', 'doesNotEqual', [])))
        records = pytest.app.records.bulk_modify(
            ('Numeric List', 'doesNotEqual', []), values={'Numeric List': Append([543])})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(
            ('Numeric List', 'contains', [543]))) == initialRecords

    def test_record_bulk_modify_append_multi_users(helpers):
        swimUser = pytest.swimlane_instance.users.get(
            display_name=pytest.tempUser1['displayName'])
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.tempUser2['displayName'])
        pytest.app.records.bulk_create({'Multi-Select Users': [swimUser]}, {'Multi-Select Users': [
                                       swimUser]}, {'Multi-Select Users': [swimUser]}, {'Multi-Select Users': [swimUser]})
        initialRecords = len(pytest.app.records.search(
            ('Multi-Select Users', 'equals', [swimUser])))
        records = pytest.app.records.bulk_modify(
            ('Multi-Select Users', 'equals', [swimUser]), values={'Multi-Select Users': Append([swimUser2])})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(
            ('Multi-Select Users', 'contains', [swimUser2]))) == initialRecords

    @pytest.mark.xfail(reason="SPT-????: There was no error about the field type, nor any changes to the value")
    def test_record_bulk_modify_append_date_time(helpers):
        baseDate = pendulum.now()
        pytest.app.records.bulk_create({'Date & Time': baseDate}, {'Date & Time': baseDate}, {
                                       'Date & Time': baseDate}, {'Date & Time': baseDate})
        initialRecords = len(pytest.app.records.search(
            ('Date & Time', 'equals', baseDate)))
        records = pytest.app.records.bulk_modify(('Date & Time', 'equals', baseDate), values={
                                                 'Date & Time': Append(pendulum.yesterday())})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(
            ('Date & Time', 'equals', baseDate))) == 0

    @pytest.mark.xfail(reason="SPT-????: There was no error about the field type, nor any changes to the value")
    def test_record_bulk_modify_append_first_created(helpers):
        baseDate = pendulum.now()
        changeDate = pendulum.tomorrow()
        pytest.app.records.bulk_create({'Date & Time': baseDate}, {'Date & Time': baseDate}, {
                                       'Date & Time': baseDate}, {'Date & Time': baseDate})
        initialRecords = len(pytest.app.records.search(
            ('Date & Time', 'equals', baseDate)))
        records = pytest.app.records.bulk_modify(('Date & Time', 'equals', baseDate), values={
                                                 'First Created': Append(changeDate)})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(
            ('First Created', 'equals', changeDate))) == 0

    @pytest.mark.xfail(reason="SPT-????: There was no error about the field type, nor any changes to the value")
    def test_record_bulk_modify_append_last_updated(helpers):
        baseDate = pendulum.now()
        changeDate = pendulum.tomorrow()
        pytest.app.records.bulk_create({'Date & Time': baseDate}, {'Date & Time': baseDate}, {
                                       'Date & Time': baseDate}, {'Date & Time': baseDate})
        initialRecords = len(pytest.app.records.search(
            ('Date & Time', 'equals', baseDate)))
        records = pytest.app.records.bulk_modify(
            ('Date & Time', 'equals', baseDate), values={'Last Updated': Append(changeDate)})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(
            ('Last Updated', 'equals', changeDate))) == 0

    @pytest.mark.xfail(reason="SPT-????: There was no error about the field type, nor any changes to the value")
    def test_record_bulk_modify_append_created_by(helpers):
        swimUser = pytest.swimlane_instance.users.get(
            display_name=pytest.tempUser1['displayName'])
        defaultText = "modify created by"
        pytest.app.records.bulk_create({'Text': defaultText}, {'Text': defaultText}, {
                                       'Text': defaultText}, {'Text': defaultText})
        initialRecords = len(pytest.app.records.search(
            ('Text', 'equals', defaultText)))
        alreadySetRecords = len(pytest.app.records.search(
            ('Created by', 'equals', swimUser)))
        records = pytest.app.records.bulk_modify(
            ('Text', 'equals', defaultText), values={'Created by': Append(swimUser)})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(
            ('Created by', 'equals', swimUser))) == initialRecords + alreadySetRecords

    @pytest.mark.xfail(reason="SPT-????: There was no error about the field type, nor any changes to the value")
    def test_record_bulk_modify_append_last_updated_by(helpers):
        swimUser = pytest.swimlane_instance.users.get(
            display_name=pytest.tempUser1['displayName'])
        defaultText = "modify last updated by"
        pytest.app.records.bulk_create({'Text': defaultText}, {'Text': defaultText}, {
                                       'Text': defaultText}, {'Text': defaultText})
        initialRecords = len(pytest.app.records.search(
            ('Text', 'equals', defaultText)))
        alreadySetRecords = len(pytest.app.records.search(
            ('Last updated by', 'equals', swimUser)))
        records = pytest.app.records.bulk_modify(('Text', 'equals', defaultText), values={
                                                 'Last updated by': Append(swimUser)})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(
            ('Last updated by', 'equals', swimUser))) == initialRecords + alreadySetRecords

    def test_record_bulk_modify_append_attachment(helpers):
        baseText = "Has Attachment"
        fileName = '6.65kB.json'
        pytest.app.records.bulk_create({'Text': baseText}, {'Text': baseText}, {
                                       'Text': baseText}, {'Text': baseText})
        theFile = pytest.helpers.loadFileStream(fileName)
        with pytest.raises(ValueError) as excinfo:
            pytest.app.records.bulk_modify(('Text', 'equals', baseText), values={
                                           'Attachment': Append(theFile)})
        assert str(
            excinfo.value) == 'Field \'Attachment\' of Type \'AttachmentsField\', is not supported for bulk modify'

    def test_record_bulk_modify_append_comments(helpers):
        baseText = "Has Comment"
        pytest.app.records.bulk_create({'Text': baseText}, {'Text': baseText}, {
                                       'Text': baseText}, {'Text': baseText})
        with pytest.raises(ValueError) as excinfo:
            pytest.app.records.bulk_modify(('Text', 'equals', baseText), values={
                                           'Attachment': Append(baseText)})
        assert str(
            excinfo.value) == 'Field \'Attachment\' of Type \'AttachmentsField\', is not supported for bulk modify'

    @pytest.mark.xfail(reason="SPT-????: There was no error about the field type, but the passed in targetRecord, which is a record class, thinks it is a tuple??")
    def test_record_bulk_modify_append_references(helpers):
        baseText = "Has Reference"
        pytest.app.records.bulk_create({'Text': baseText}, {'Text': baseText}, {
                                       'Text': baseText}, {'Text': baseText})
        targetApp = pytest.swimlane_instance.apps.get(
            name="PYTHON-Helpers Target App")
        targetRecord = targetApp.records.create()
        records = pytest.app.records.bulk_modify(('Text', 'equals', baseText), values={
                                                 'Reference': Append(targetRecord)})
        pytest.waitOnJobByID(records)
        for record in pytest.app.records.search(('Text', 'equals', baseText)):
            assert len(record['Reference']) == 1


class TestRecordAdaptorBulkModifyRemove:
    def test_record_bulk_modify_remove_text(helpers):
        pytest.app.records.bulk_create({'Text': 'hello'}, {'Text': 'hello goodbye'}, {
                                       'Text': 'goodbye'}, {'Text': 'hello goodbye fred'})
        records = pytest.app.records.bulk_modify(
            ('Text', 'contains', 'hello'), values={'Text': Remove("hello")})
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search(
            ('Text', 'contains', "hello"))) == 0

    @pytest.mark.xfail(reason="SPT-????: There was no error about the field type, nor any changes to the value")
    def test_record_bulk_modify_remove_numeric(helpers):
        pytest.app.records.bulk_create({'Numeric': 123}, {'Numeric': 123}, {
                                       'Numeric': 123}, {'Numeric': 1234})
        records = pytest.app.records.bulk_modify(
            ('Numeric', 'equals', 123), values={'Numeric': Remove(123)})
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search(('Numeric', 'equals', 123))) == 0

    @pytest.mark.xfail(reason="SPT-????: There was no error about the field type, nor any changes to the value")
    def test_record_bulk_modify_remove_selection(helpers):
        pytest.app.records.bulk_create({'Selection': 'New Value'}, {'Selection': 'New Value'}, {
                                       'Selection': 'New Value'}, {'Selection': 'New Value'})
        initialRecords = len(pytest.app.records.search(
            ('Selection', 'equals', 'New Value')))
        alreadySetRecords = len(pytest.app.records.search(
            ('Selection', 'equals', None)))
        records = pytest.app.records.bulk_modify(
            ('Selection', 'equals', 'New Value'), values={'Selection': Remove('New Value')})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 3
        assert len(pytest.app.records.search(
            ('Selection', 'equals', None))) == initialRecords + alreadySetRecords

    def test_record_bulk_modify_remove_multi_selection(helpers):
        pytest.app.records.bulk_create({'Multi-select': ['one', 'three']}, {'Multi-select': [
                                       'one', 'three']}, {'Multi-select': ['one', 'three']}, {'Multi-select': ['one', 'three']})
        records = pytest.app.records.bulk_modify(
            ('Multi-select', 'contains', ['three']), values={'Multi-select': Remove(["three"])})
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search(
            ('Multi-select', 'contains', ["three"]))) == 0

    @pytest.mark.xfail(reason="SPT-????: IS the bulk modify not removing text list item if it is the last item???")
    def test_record_bulk_modify_remove_text_list(helpers):
        pytest.app.records.bulk_create({'Text List': ['bob']}, {'Text List': ['bob', 'goodbye']}, {
                                       'Text List': ['bob']}, {'Text List': ['bob', 'goodbye', 'fred']})
        records = pytest.app.records.bulk_modify(
            ('Text List', 'contains', ['bob']), values={'Text List': Remove(["bob"])})
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search(
            ('Text List', 'contains', ["bob"]))) == 0

    @pytest.mark.xfail(reason="SPT-????: IS the bulk modify not removing numeric list item if it is the last item???")
    def test_record_bulk_modify_remove_numeric_list(helpers):
        pytest.app.records.bulk_create({'Numeric List': [123]}, {'Numeric List': [123, 456]}, {
                                       'Numeric List': [456, 123]}, {'Numeric List': [123, 456, 789]})
        records = pytest.app.records.bulk_modify(
            ('Numeric List', 'contains', [123]), values={'Numeric List': Remove([123])})
        pytest.waitOnJobByID(records)
        assert len(pytest.app.records.search(
            ('Numeric List', 'contains', [123]))) == 0

    def test_record_bulk_modify_remove_multi_users(helpers):
        swimUser = pytest.swimlane_instance.users.get(
            display_name=pytest.tempUser1['displayName'])
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.tempUser2['displayName'])
        pytest.app.records.bulk_create({'Multi-Select Users': [swimUser]}, {'Multi-Select Users': [swimUser2]}, {
                                       'Multi-Select Users': [swimUser, swimUser2]}, {'Multi-Select Users': [swimUser, swimUser2]})
        initialRecords = len(pytest.app.records.search(
            ('Multi-Select Users', 'contains', [swimUser2]), ('Multi-Select Users', 'excludes', [swimUser])))
        records = pytest.app.records.bulk_modify(
            ('Multi-Select Users', 'contains', [swimUser]), values={'Multi-Select Users': Remove([swimUser2])})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 1
        assert len(pytest.app.records.search(
            ('Multi-Select Users', 'contains', [swimUser2]))) == initialRecords

    @pytest.mark.xfail(reason="SPT-????: There was no error about the field type, nor any changes to the value")
    def test_record_bulk_modify_remove_date_time(helpers):
        baseDate = pendulum.now()
        pytest.app.records.bulk_create({'Date & Time': baseDate}, {'Date & Time': baseDate}, {
                                       'Date & Time': baseDate}, {'Date & Time': baseDate})
        initialRecords = len(pytest.app.records.search(
            ('Date & Time', 'equals', baseDate)))
        records = pytest.app.records.bulk_modify(
            ('Date & Time', 'equals', baseDate), values={'Date & Time': Remove(baseDate)})
        pytest.waitOnJobByID(records)
        assert initialRecords >= 4
        assert len(pytest.app.records.search(
            ('Date & Time', 'equals', baseDate))) == 0

    @pytest.mark.xfail(reason="SPT-????: There was no error about the field type, nor any changes to the value")
    def test_record_bulk_modify_remove_first_created(helpers):
        baseDate = pendulum.now()
        pytest.app.records.bulk_create({'Date & Time': baseDate}, {'Date & Time': baseDate}, {
                                       'Date & Time': baseDate}, {'Date & Time': baseDate})
        initialRecords = pytest.app.records.search(
            ('Date & Time', 'equals', baseDate))
        createdDate = initialRecords[0]['First Created']
        records = pytest.app.records.bulk_modify(('Date & Time', 'equals', baseDate), values={
                                                 'First Created': Remove(createdDate)})
        pytest.waitOnJobByID(records)
        assert len(initialRecords) >= 4
        assert len(pytest.app.records.search(
            ('First Created', 'equals', createdDate))) == 0

    @pytest.mark.xfail(reason="SPT-????: There was no error about the field type, nor any changes to the value")
    def test_record_bulk_modify_remove_last_updated(helpers):
        baseDate = pendulum.now()
        pytest.app.records.bulk_create({'Date & Time': baseDate}, {'Date & Time': baseDate}, {
                                       'Date & Time': baseDate}, {'Date & Time': baseDate})
        initialRecords = pytest.app.records.search(
            ('Date & Time', 'equals', baseDate))
        updatedDate = initialRecords[0]['Last Updated']
        records = pytest.app.records.bulk_modify(('Date & Time', 'equals', baseDate), values={
                                                 'Last Updated': Remove(updatedDate)})
        pytest.waitOnJobByID(records)
        assert len(initialRecords) >= 4
        assert len(pytest.app.records.search(
            ('Last Updated', 'equals', updatedDate))) == 0

    @pytest.mark.xfail(reason="SPT-????: There was no error about the field type, nor any changes to the value")
    def test_record_bulk_modify_remove_created_by(helpers):
        defaultText = "remove created by"
        pytest.app.records.bulk_create({'Text': defaultText}, {'Text': defaultText}, {
                                       'Text': defaultText}, {'Text': defaultText})
        initialRecords = pytest.app.records.search(
            ('Text', 'equals', defaultText))
        createdByUser = initialRecords[0]['Created by']
        alreadySetRecords = len(pytest.app.records.search(
            ('Created by', 'equals', None)))
        records = pytest.app.records.bulk_modify(('Text', 'equals', defaultText), values={
                                                 'Created by': Remove(createdByUser)})
        pytest.waitOnJobByID(records)
        assert len(initialRecords) >= 4
        assert len(pytest.app.records.search(
            ('Created by', 'equals', None))) == len(initialRecords) + alreadySetRecords

    @pytest.mark.xfail(reason="SPT-????: There was no error about the field type, nor any changes to the value")
    def test_record_bulk_modify_remove_last_updated_by(helpers):
        defaultText = "remove last updated by"
        pytest.app.records.bulk_create({'Text': defaultText}, {'Text': defaultText}, {
                                       'Text': defaultText}, {'Text': defaultText})
        initialRecords = pytest.app.records.search(
            ('Text', 'equals', defaultText))
        updatedByUser = initialRecords[0]['Created by']
        alreadySetRecords = len(pytest.app.records.search(
            ('Last updated by', 'equals', None)))
        records = pytest.app.records.bulk_modify(('Text', 'equals', defaultText), values={
                                                 'Last updated by': Remove(updatedByUser)})
        pytest.waitOnJobByID(records)
        assert len(initialRecords) >= 4
        assert len(pytest.app.records.search(('Last updated by', 'equals', None))) == len(
            initialRecords) + alreadySetRecords

    def test_record_bulk_modify_remove_attachment(helpers):
        baseText = "remove Attachment"
        fileName = '6.65kB.json'
        pytest.app.records.bulk_create({'Text': baseText}, {'Text': baseText}, {
                                       'Text': baseText}, {'Text': baseText})
        theFile = pytest.helpers.loadFileStream(fileName)
        with pytest.raises(ValueError) as excinfo:
            pytest.app.records.bulk_modify(('Text', 'equals', baseText), values={
                'Attachment': Remove(theFile)})
        assert str(
            excinfo.value) == 'Field \'Attachment\' of Type \'AttachmentsField\', is not supported for bulk modify'

    def test_record_bulk_modify_remove_comments(helpers):
        baseText = "Has Comment"
        pytest.app.records.bulk_create({'Text': baseText}, {'Text': baseText}, {
                                       'Text': baseText}, {'Text': baseText})
        with pytest.raises(ValueError) as excinfo:
            pytest.app.records.bulk_modify(('Text', 'equals', baseText), values={
                'Attachment': Remove(baseText)})
        assert str(
            excinfo.value) == 'Field \'Attachment\' of Type \'AttachmentsField\', is not supported for bulk modify'

    @pytest.mark.xfail(reason="SPT-????: There was no error about the field type, but the passed in targetRecord, which is a record class, thinks it is a tuple??")
    def test_record_bulk_modify_remove_references(helpers):
        baseText = "Has Reference"
        pytest.app.records.bulk_create({'Text': baseText}, {'Text': baseText}, {
                                       'Text': baseText}, {'Text': baseText})
        targetApp = pytest.swimlane_instance.apps.get(
            name="PYTHON-Helpers Target App")
        targetRecord = targetApp.records.create()
        records = pytest.app.records.bulk_modify(('Text', 'equals', baseText), values={
                                                 'Reference': Remove(targetRecord)})
        pytest.waitOnJobByID(records)
        for record in pytest.app.records.search(('Text', 'equals', baseText)):
            assert len(record['Reference']) == 1

    def test_record_bulk_modify_remove_multiple_text_list(helpers):
        textForFilter = "text list remove multiple"
        pytest.app.records.bulk_create(
            {'Text': textForFilter, 'Text List': [
                'a', 'b', 'c', 'd', 'e', 'a']},
            {'Text': textForFilter, 'Text List': ['a', 'b', 'c', 'd', 'e']},
            {'Text': textForFilter, 'Text List': ['a', 'b', 'c']},
            {'Text': textForFilter, 'Text List': ['b', 'c', 'd', 'e']})
        originalRecords = pytest.app.records.search(
            ('Text', 'equals', textForFilter))
        recordedListValues = {}
        for record in originalRecords:
            recordedListValues[record.id] = list(record['Text List'])

        records = pytest.app.records.bulk_modify(
            ('Text', 'equals', textForFilter), values={'Text List': Remove(['a', 'd'])})
        pytest.waitOnJobByID(records)
        updatedRecords = pytest.app.records.search(
            ('Text', 'equals', textForFilter))

        for record in updatedRecords:
            listDiff = list(
                set(recordedListValues[record.id]) - set(list(record['Text List'])))
            assert (all(elem in ['a', 'd'] for elem in listDiff))

    def test_record_bulk_modify_remove_multiple_numeric_list(helpers):
        textForFilter = "numeric list remove multiple"
        pytest.app.records.bulk_create(
            {'Text': textForFilter, 'Numeric List': [1, 2, 3, 4, 5, 1]},
            {'Text': textForFilter, 'Numeric List': [1, 2, 3, 4, 5]},
            {'Text': textForFilter, 'Numeric List': [1, 2, 3]},
            {'Text': textForFilter, 'Numeric List': [2, 3, 4, 5]})
        originalRecords = pytest.app.records.search(
            ('Text', 'equals', textForFilter))
        recordedListValues = {}
        for record in originalRecords:
            recordedListValues[record.id] = list(record['Numeric List'])

        records = pytest.app.records.bulk_modify(
            ('Text', 'equals', textForFilter), values={'Numeric List': Remove([1, 4])})
        pytest.waitOnJobByID(records)
        updatedRecords = pytest.app.records.search(
            ('Text', 'equals', textForFilter))

        for record in updatedRecords:
            listDiff = list(
                set(recordedListValues[record.id]) - set(list(record['Numeric List'])))
            assert (all(elem in [1, 4] for elem in listDiff))
