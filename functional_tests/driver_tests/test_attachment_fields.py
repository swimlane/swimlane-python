import pytest
from swimlane import exceptions
from io import BytesIO
# Not testing the TTL on attachment fields.

@pytest.fixture(autouse=True, scope='module')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'attachment fields'
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.app, pytest.appid =  helpers.findCreateApp(defaultApp)
    pytest.helpers = helpers
    yield
    # teardown stuff
    helpers.cleanupData()

class TestAttachmentField:
    def test_attachment_field_value(helpers):
        theRecord = pytest.app.records.create(**{})
        assert len(theRecord['Attachment']) == 0

    def test_attachment_field_add_file(helpers):
        fileName = '277kb.jpg'
        theRecord = pytest.app.records.create(**{})
        theFile = pytest.helpers.loadFileStream(fileName)
        theRecord['Attachment'].add(fileName, theFile)
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord['Attachment']) == 1
        attachment = updatedRecord['Attachment'][0]
        assert attachment.filename == fileName
        assert len(attachment.download().read()) > 0

    def test_attachment_field_add_file_no_name(helpers):
        fileName = '277kb.jpg'
        theRecord = pytest.app.records.create(**{})
        theFile = pytest.helpers.loadFileStream(fileName)
        with pytest.raises(TypeError) as excinfo:
            theRecord['Attachment'].add(None, theFile)
        assert str(excinfo.value) == 'expected {}'.format('string or buffer' if (pytest.helpers.py_ver() == 2) else 'string or bytes-like object')
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord['Attachment']) == 0

    @pytest.mark.xfail(reason="SPT-6351: Should make sure the name is not empty, gets 500 from API call")
    def test_attachment_field_add_file_empty_name(helpers):
        fileName = '277kb.jpg'
        theRecord = pytest.app.records.create(**{})
        theFile = pytest.helpers.loadFileStream(fileName)
        # with pytest.raises(TypeError) as excinfo:
        theRecord['Attachment'].add('', theFile)
        # assert str(excinfo.value) == 'expected string or buffer'
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord['Attachment']) == 0

    @pytest.mark.xfail(reason="SPT-6351: Should make sure the file is not empty, gets 500 from API call")
    def test_attachment_field_add_file_no_file(helpers):
        fileName = '277kb.jpg'
        theRecord = pytest.app.records.create(**{})
        # with pytest.raises(TypeError) as excinfo:
        theRecord['Attachment'].add(fileName, None)
        # assert str(excinfo.value) == 'expected string or buffer'
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord['Attachment']) == 0

    @pytest.mark.xfail(reason="SPT-6351: Should make sure the file is not empty, gets 500 from API call")
    def test_attachment_field_add_file_empty_file(helpers):
        fileName = '277kb.jpg'
        theRecord = pytest.app.records.create(**{})
        # with pytest.raises(TypeError) as excinfo:
        theRecord['Attachment'].add(fileName, BytesIO())
        # assert str(excinfo.value) == 'expected string or buffer'
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord['Attachment']) == 1

    def test_attachment_field_add_file_just_file(helpers):
        fileName = '277kb.jpg'
        theRecord = pytest.app.records.create(**{})
        theFile = pytest.helpers.loadFileStream(fileName)
        with pytest.raises(TypeError) as excinfo:
            theRecord['Attachment'].add(theFile)
        assert str(excinfo.value) == 'add() {}'.format(pytest.helpers.py_ver_missing_param(3,2,"stream"))
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord['Attachment']) == 0

    def test_attachment_field_remove_all(helpers):
        fileName = '277kb.jpg'
        fileName2 = 'Python Driver Setup Instructions.rtf'
        theRecord = pytest.app.records.create(**{})
        theFile = pytest.helpers.loadFileStream(fileName)
        theFile2 = pytest.helpers.loadFileStream(fileName2)
        theRecord['Attachment'].add(fileName, theFile)
        theRecord['Attachment'].add(fileName2, theFile2)
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord['Attachment']) == 2
        theRecord['Attachment'] = None
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord['Attachment']) == 0

    def test_attachment_field_needs_save(helpers):
        fileName = '277kb.jpg'
        fileName2 = 'Python Driver Setup Instructions.rtf'
        theRecord = pytest.app.records.create(**{})
        theFile = pytest.helpers.loadFileStream(fileName)
        theFile2 = pytest.helpers.loadFileStream(fileName2)
        theRecord['Attachment'].add(fileName, theFile)
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord['Attachment']) == 1
        theRecord['Attachment'].add(fileName2, theFile2)
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord['Attachment']) == 1

class TestReadOnlyAttachmentField:
    def test_read_only_attachment_field(helpers):
        fileName = '277kb.jpg'
        theRecord = pytest.app.records.create(**{})
        theFile = pytest.helpers.loadFileStream(fileName)
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord['ReadOnly Attachment'].add(fileName, theFile)
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Cannot set readonly field \'ReadOnly Attachment\'' % theRecord.tracking_id
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord['Attachment']) == 0

class TestMaxSizeAttachmentFiled:
    def test_max_size_attachment_field_small_enough(helpers):
        fileName = '5.35kB.json'
        theRecord = pytest.app.records.create(**{})
        theFile = pytest.helpers.loadFileStream(fileName)
        theRecord['Attachment'].add(fileName, theFile)
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord['Attachment']) == 1
        attachment = updatedRecord['Attachment'][0]
        assert attachment.filename == fileName
        assert len(attachment.download().read()) > 0

    @pytest.mark.xfail(reason="SPT-6358:Not honoring file size. Should pyDriver try to check?")
    def test_max_size_attachment_field_too_big(helpers):
        fileName = '5.74kB.json'
        theRecord = pytest.app.records.create(**{})
        theFile = pytest.helpers.loadFileStream(fileName)
        theRecord['Attachment'].add(fileName, theFile)
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord['Attachment']) == 1
        attachment = updatedRecord['Attachment'][0]
        assert attachment.filename == fileName
        assert len(attachment.download().read()) > 0
