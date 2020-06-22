import pytest

# patch


@pytest.fixture(autouse=True, scope='session')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'QA-PyDriver App'
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.waitOnJobByID = helpers.waitOnJobByID
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    pytest.tempUser = helpers.createUser()
    pytest.tempGroup = helpers.createGroup()
    yield
    # teardown stuff
    helpers.cleanupData()


class TestRecordAdaptorPatch:
    def test_record_patch_text(helpers):
        recordToPatch = pytest.app.records.create(
            **{'Numeric List': [123], 'Text': 'r2d2', 'Multi-select': 'a'})
        patchedRecordID = recordToPatch.id
        recordBeforePatch = pytest.app.records.get(id=patchedRecordID)
        recordBeforePatch['Numeric List'] = [777]
        recordBeforePatch.save()

        recordToPatch['Text'] = 'c3po'
        recordToPatch.patch()

        patchedRecord = pytest.app.records.get(id=patchedRecordID)
        assert list(recordBeforePatch['Numeric List']) == [777]
        assert list(recordToPatch['Numeric List']) == [777]
        assert recordToPatch['Numeric List'] == patchedRecord['Numeric List']
        assert recordToPatch['Multi-select'] == patchedRecord['Multi-select']
        assert recordToPatch['Text'] == patchedRecord['Text']

    def test_record_patch_numeric_list(helpers):
        recordToPatch = pytest.app.records.create(
            **{'Numeric List': [123], 'Text': 'r2d2', 'Multi-select': 'a'})
        recordID = recordToPatch.id
        recordToPatch['Numeric List'] = [456]
        recordToPatch.patch()

        patchedRecord = pytest.app.records.get(id=recordID)
        assert dict(recordToPatch) == dict(patchedRecord)

    def test_record_patch_multi_select(helpers):
        recordToPatch = pytest.app.records.create(
            **{'Numeric List': [123], 'Text': 'r2d2', 'Multi-select': 'a'})
        recordID = recordToPatch.id
        recordToPatch['Multi-select'].select('b')
        recordToPatch['Multi-select'].select('c')
        recordToPatch['Multi-select'].deselect('a')
        recordToPatch.patch()

        patchedRecord = pytest.app.records.get(id=recordID)
        assert dict(recordToPatch) == dict(patchedRecord)

    def test_record_patch_users_groups(helpers):
        swimUser = pytest.swimlane_instance.users.get(
            id=pytest.tempUser['id']).resolve()
        adminUser = pytest.swimlane_instance.users.get(display_name='admin')

        recordToPatch = pytest.app.records.create(
            **{'Numeric List': [123], 'Text': 'r2d2', 'User/Groups': adminUser})
        recordID = recordToPatch.id
        recordToPatch['User/Groups'] = swimUser
        recordToPatch.patch()

        patchedRecord = pytest.app.records.get(id=recordID)
        assert dict(recordToPatch) == dict(patchedRecord)

    def test_record_patch_multiple_fields(helpers):
        recordToPatch = pytest.app.records.create(
            **{'Numeric List': [123], 'Text': 'r2d2', 'Multi-select': 'a'})
        recordID = recordToPatch.id
        recordToPatch['Text'] = 'IG-11'
        recordToPatch['Numeric List'] = [456, 111, 222]
        recordToPatch['Multi-select'].select('c')
        recordToPatch['Multi-select'].deselect('a')
        recordToPatch.patch()

        patchedRecord = pytest.app.records.get(id=recordID)
        assert dict(recordToPatch) == dict(patchedRecord)

    @pytest.mark.xfail(reason="Valid Errors: Verify unable to update readonly field in record using patch call")
    def test_record_patch_readonly(helpers):
        recordToPatch = pytest.app.records.create(
            **{'Numeric List': [123], 'Text': 'r2d2', 'Multi-select': 'a'})
        recordID = recordToPatch.id
        recordToPatch['NumericReadOnly'] = 12
        recordToPatch.patch()

        patchedRecord = pytest.app.records.get(id=recordID)
        assert dict(recordToPatch) == dict(patchedRecord)
