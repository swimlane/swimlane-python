import pytest
from swimlane import exceptions

# add_comment
# add_record_references
# check_bulk_job_status


@pytest.fixture(autouse=True, scope='session')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'Helpers Source App'
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.helpers = helpers
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    pytest.targetApp = pytest.swimlane_instance.apps.get(
        name="PYTHON-%s" % helpers.appPairings[defaultApp])
    pytest.targetRecord = pytest.targetApp.records.create(
        **{'Text': pytest.fake.sentence()})
    pytest.CommentFieldID = pytest.app.get_field_definition_by_name('Comments')[
        'id']
    pytest.textFieldID = pytest.app.get_field_definition_by_name('Text')['id']
    pytest.refFieldID = pytest.app.get_field_definition_by_name('Reference')[
        'id']
    pytest.waitOnJobByID = helpers.waitOnJobByID
    yield
    # teardown stuff
    helpers.cleanupData()


class TestHelpersAddCommentAdaptor:
    def test_add_first_comment(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        commentText = pytest.fake.sentence()
        pytest.swimlane_instance.helpers.add_comment(
            pytest.app.id, sourceRecord.id, pytest.CommentFieldID, commentText)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert editedRecord['Comments'][-1].message == commentText
        assert len(editedRecord['Comments']) == 1

    def test_add_nth_comment(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        commentText = pytest.fake.sentence()
        pytest.swimlane_instance.helpers.add_comment(
            pytest.app.id, sourceRecord.id, pytest.CommentFieldID, commentText)
        commentText2 = pytest.fake.sentence()
        pytest.swimlane_instance.helpers.add_comment(
            pytest.app.id, sourceRecord.id, pytest.CommentFieldID, commentText2)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert editedRecord['Comments'][-1].message == commentText2
        assert editedRecord['Comments'][-2].message == commentText

    def test_add_rich_text_comment(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        commentText = pytest.fake.sentence()
        pytest.swimlane_instance.helpers.add_comment(
            pytest.app.id, sourceRecord.id, pytest.CommentFieldID, commentText)
        commentText2 = '<p>{}</p>'.format(pytest.fake.sentence())
        pytest.swimlane_instance.helpers.add_comment(
            pytest.app.id, sourceRecord.id, pytest.CommentFieldID, commentText2, True)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert editedRecord['Comments'][-1].message == commentText2
        assert editedRecord['Comments'][-1].is_rich_text == True
        assert editedRecord['Comments'][-2].message == commentText
        assert editedRecord['Comments'][-2].is_rich_text == False

    def test_add_rich_text_not_bool_comment(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        commentText = pytest.fake.sentence()
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.helpers.add_comment(
                pytest.app.id, sourceRecord.id, pytest.CommentFieldID, commentText, 123)
        assert str(excinfo.value) == "rich_text must be a boolean value."

    @pytest.mark.xfail(reason="SPT-6196: Message Value is not checked for valid test.")
    def test_comment_empty(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        commentText = ''
        pytest.swimlane_instance.helpers.add_comment(
            pytest.app.id, sourceRecord.id, pytest.CommentFieldID, commentText)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert editedRecord['Comments'][-1].message == commentText

    @pytest.mark.xfail(reason="SPT-6195: Message Value is not checked for valid test.")
    def test_comment_none(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        commentText = None
        pytest.swimlane_instance.helpers.add_comment(
            pytest.app.id, sourceRecord.id, pytest.CommentFieldID, commentText)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert editedRecord['Comments'][-1].message == commentText

    @pytest.mark.xfail(reason="SPT-6195: Message Value is not checked for valid test.")
    def test_comment_number(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        commentText = 123
        pytest.swimlane_instance.helpers.add_comment(
            pytest.app.id, sourceRecord.id, pytest.CommentFieldID, commentText)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert editedRecord['Comments'][-1].message == commentText

    @pytest.mark.xfail(reason="SPT-6195: Message Value is not checked for valid test.")
    def test_comment_object(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        commentText = {'Name': 'Fred'}
        pytest.swimlane_instance.helpers.add_comment(
            pytest.app.id, sourceRecord.id, pytest.CommentFieldID, commentText)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert editedRecord['Comments'][-1].message == commentText

    def test_comment_missing(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        with pytest.raises(TypeError) as excinfo:
            pytest.swimlane_instance.helpers.add_comment(
                pytest.app.id, sourceRecord.id, pytest.CommentFieldID)
        assert str(excinfo.value) == 'add_comment() {}'.format(
            pytest.helpers.py_ver_missing_param(5, 4, "message", "at least"))

    @pytest.mark.xfail(reason="SPT-6196: Pydriver should verify that the commentFieldID should be a valid value")
    def test_comment_empty_fieldId(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        commentText = pytest.fake.sentence()
        commendFieldId = ''
        pytest.swimlane_instance.helpers.add_comment(
            pytest.app.id, sourceRecord.id, commendFieldId, commentText)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert editedRecord['Comments'][-1].message == commentText

    @pytest.mark.xfail(reason="SPT-6196: Pydriver should verify that the recordID should be a valid value")
    def test_comment_empty_recordId(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        commentText = pytest.fake.sentence()
        recordId = ''
        pytest.swimlane_instance.helpers.add_comment(
            pytest.app.id, recordId, pytest.CommentFieldID, commentText)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert editedRecord['Comments'][-1].message == commentText

    @pytest.mark.xfail(reason="SPT-6196: Pydriver should verify that the appID should be a valid value")
    def test_comment_empty_appId(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        commentText = pytest.fake.sentence()
        appId = ''
        pytest.swimlane_instance.helpers.add_comment(
            appId, sourceRecord.id, pytest.CommentFieldID, commentText)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert len(editedRecord['Comments']) == 0

    def test_comment_missmatch_appid(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        commentText = pytest.fake.sentence()
        pytest.swimlane_instance.helpers.add_comment(
            pytest.targetApp.id, sourceRecord.id, pytest.CommentFieldID, commentText)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert len(editedRecord['Comments']) == 1
        assert editedRecord['Comments'][-1].message == commentText

    @pytest.mark.xfail(reason="SPT-6248: This should fail because the recordID is from a different app")
    def test_comment_missmatch_recordid(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        commentText = pytest.fake.sentence()
        pytest.swimlane_instance.helpers.add_comment(
            pytest.app.id, pytest.targetRecord.id, pytest.CommentFieldID, commentText)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert len(editedRecord['Comments']) == 0

    @pytest.mark.xfail(reason="SPT-6248: This should fail because the commentFieldID is not a comment field")
    def test_comment_missmatch_fieldid(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        commentText = pytest.fake.sentence()
        pytest.swimlane_instance.helpers.add_comment(
            pytest.app.id, sourceRecord.id, pytest.textFieldID, commentText)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert len(editedRecord['Comments']) == 0

    @pytest.mark.xfail(reason="SPT-6196: Pydriver should verify the IDs are valid input.")
    def test_comment_app_object(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        commentText = pytest.fake.sentence()
        pytest.swimlane_instance.helpers.add_comment(
            pytest.app, sourceRecord.id, pytest.CommentFieldID, commentText)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert len(editedRecord['Comments']) == 0

    @pytest.mark.xfail(reason="SPT-6196: Pydriver should verify the IDs are valid input.")
    def test_comment_record_object(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        commentText = pytest.fake.sentence()
        pytest.swimlane_instance.helpers.add_comment(
            pytest.app.id, sourceRecord, pytest.CommentFieldID, commentText)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert len(editedRecord['Comments']) == 0


class TestHelpersAddRefernceAdaptor:
    def test_addReference(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        currentRefCount = len(pytest.app.records.get(
            id=sourceRecord.id)['Reference'])
        pytest.swimlane_instance.helpers.add_record_references(
            pytest.app.id, sourceRecord.id, pytest.refFieldID, [pytest.targetRecord.id])
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert editedRecord['Reference'][-1] == pytest.targetRecord
        assert len(editedRecord['Reference']) == currentRefCount + 1

    def test_addReference_empty_list(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        recordsToAddRef = []
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.helpers.add_record_references(
                pytest.app.id, sourceRecord.id, pytest.refFieldID, recordsToAddRef)
        assert str(excinfo.value) == "target_record_ids must be a non-empty list value"

    def test_addReference_list_empty_str(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        recordsToAddRef = ['']
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.helpers.add_record_references(
                pytest.app.id, sourceRecord.id, pytest.refFieldID, recordsToAddRef)
        assert str(excinfo.value) == "target_record_ids must contain non-empty string values"
    
    def test_addReference_list_int(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        recordsToAddRef = [123]
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.helpers.add_record_references(
                pytest.app.id, sourceRecord.id, pytest.refFieldID, recordsToAddRef)
        assert str(excinfo.value) == "target_record_ids must contain non-empty string values"

    def test_addReference_list_dict(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        recordsToAddRef = [{'test':'dict'}]
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.helpers.add_record_references(
                pytest.app.id, sourceRecord.id, pytest.refFieldID, recordsToAddRef)
        assert str(excinfo.value) == "target_record_ids must contain non-empty string values"
    
    def test_addReference_not_list(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        recordsToAddRef = 123
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.helpers.add_record_references(
                pytest.app.id, sourceRecord.id, pytest.refFieldID, recordsToAddRef)
        assert str(excinfo.value) == "target_record_ids must be a non-empty list value"

    @pytest.mark.xfail(reason="SPT-6242: Verify record to add to ref field. Bombs out on the assert line.")
    def test_addReference_record_from_wrong_app(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        currentRefCount = len(pytest.app.records.get(
            id=sourceRecord.id)['Reference'])
        recordsToAddRef = [sourceRecord.id]
        pytest.swimlane_instance.helpers.add_record_references(
            pytest.app.id, sourceRecord.id, pytest.refFieldID, recordsToAddRef)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert len(editedRecord['Reference']) == currentRefCount

    def test_addReference_no_refs_passed(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        with pytest.raises(TypeError) as excinfo:
            pytest.swimlane_instance.helpers.add_record_references(
                pytest.app.id, sourceRecord.id, pytest.refFieldID)
        assert str(excinfo.value) == 'add_record_references() {}'.format(
            pytest.helpers.py_ver_missing_param(5, 4, "target_record_ids", "exactly"))

    def test_addReference_wrong_app_id(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        currentRefCount = len(pytest.app.records.get(
            id=sourceRecord.id)['Reference'])
        recordsToAddRef = [pytest.targetRecord.id]
        with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
            pytest.swimlane_instance.helpers.add_record_references(
                pytest.targetApp.id, sourceRecord.id, pytest.refFieldID, recordsToAddRef)
        assert str(excinfo.value) == 'ModelValidationError:5008 (%s): Bad Request for url: %s/api/app/%s/record/%s/add-references' % (
            pytest.refFieldID, pytest.helpers.url, pytest.targetApp.id, sourceRecord.id)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert len(editedRecord['Reference']) == currentRefCount

    @pytest.mark.xfail(reason="SPT-6244: add_record_references API call should fail out.")
    def test_addReference_wrong_source_record_id(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        currentRefCount = len(pytest.app.records.get(
            id=sourceRecord.id)['Reference'])
        recordsToAddRef = [pytest.targetRecord.id]
        pytest.swimlane_instance.helpers.add_record_references(
            pytest.app.id, pytest.targetRecord.id, pytest.refFieldID, recordsToAddRef)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert len(editedRecord['Reference']) == currentRefCount

    def test_addReference_wrong_ref_field_id(helpers):
        sourceRecord = pytest.app.records.create(
            **{'Text': pytest.fake.sentence()})
        currentRefCount = len(pytest.app.records.get(
            id=sourceRecord.id)['Reference'])
        recordsToAddRef = [pytest.targetRecord.id]
        with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
            pytest.swimlane_instance.helpers.add_record_references(
                pytest.app.id, sourceRecord.id, pytest.textFieldID, recordsToAddRef)
        assert str(excinfo.value) == 'ModelValidationError:5008 (%s): Bad Request for url: %s/api/app/%s/record/%s/add-references' % (
            pytest.textFieldID, pytest.helpers.url, pytest.app.id, sourceRecord.id)
        editedRecord = pytest.app.records.get(id=sourceRecord.id)
        assert len(editedRecord['Reference']) == currentRefCount


class TestHelpersBulkJobStatusAdaptor:
    def test_check_bulk_status(helpers):
        pytest.targetApp.records.bulk_create(
            {}, {}, {}, {}, {}, {}, {}, {}, {})
        bulkJobID = pytest.targetApp.records.bulk_modify(
            ('Text', 'equals', None), values={'Text': '98765'})
        pytest.waitOnJobByID(bulkJobID)
        loggingStuff = pytest.swimlane_instance.helpers.check_bulk_job_status(
            bulkJobID)
        assert len(loggingStuff) > 0

    @pytest.mark.xfail(reason="SPT-6233: Should verify the bulkJobID is a non-empty string.")
    def test_check_bulk_status_null_id(helpers):
        bulkJobID = None
        loggingStuff = pytest.swimlane_instance.helpers.check_bulk_job_status(
            bulkJobID)
        assert len(loggingStuff) == 0

    @pytest.mark.xfail(reason="SPT-6233: Should verify the bulkJobID is a non-empty string.")
    def test_check_bulk_status_empty_id(helpers):
        bulkJobID = ''
        loggingStuff = pytest.swimlane_instance.helpers.check_bulk_job_status(
            bulkJobID)
        assert len(loggingStuff) == 0

    def test_check_bulk_status_no_params(helpers):
        with pytest.raises(TypeError) as excinfo:
            pytest.swimlane_instance.helpers.check_bulk_job_status()
        assert str(excinfo.value) == 'check_bulk_job_status() {}'.format(
            pytest.helpers.py_ver_missing_param(2, 1, "job_id", "exactly"))

    def test_check_bulk_status_garbage_id(helpers):
        bulkJobID = 'garbage'
        loggingStuff = pytest.swimlane_instance.helpers.check_bulk_job_status(
            bulkJobID)
        assert len(loggingStuff) == 0

    @pytest.mark.xfail(reason="SPT-6233: Should verify the bulkJobID is a non-empty string.")
    def test_check_bulk_status_numeric_id(helpers):
        bulkJobID = 1.5
        loggingStuff = pytest.swimlane_instance.helpers.check_bulk_job_status(
            bulkJobID)
        assert len(loggingStuff) == 0

    @pytest.mark.xfail(reason="SPT-6233: Should verify the bulkJobID is a non-empty string.")
    def test_check_bulk_status_object_id(helpers):
        bulkJobID = {'name': 'bob'}
        loggingStuff = pytest.swimlane_instance.helpers.check_bulk_job_status(
            bulkJobID)
        assert len(loggingStuff) == 0
