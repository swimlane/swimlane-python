import pytest
from swimlane import exceptions


@pytest.fixture(autouse=True, scope='module')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'read only field'
    pytest.helpers = helpers
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.waitOnJobByID = helpers.waitOnJobByID
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    pytest.records = []
    yield
    # teardown stuff
    helpers.cleanupData()


class Test_SPT_4287_readonly_override:
    def test_readonly_failuire(helpers):
        fullRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        assert fullRecord.created == fullRecord.modified
        assert len(fullRecord.revisions.get_all()) == 1
        with pytest.raises(exceptions.ValidationError) as excinfo:
            fullRecord['Read Only Numeric'] = 5
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Cannot set readonly field "Read Only Numeric"' % fullRecord.tracking_id

    def test_readonly_override_set(helpers):
        new_instance = pytest.helpers.reconnect_swimlane(
            write_to_read_only=True)
        current_app = new_instance.apps.get(id=pytest.appid)
        fullRecord = current_app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        assert fullRecord.created == fullRecord.modified
        assert len(fullRecord.revisions.get_all()) == 1
        fullRecord['Read Only Numeric'] = 5
        fullRecord.save()
        assert fullRecord.created < fullRecord.modified
        assert len(fullRecord.revisions.get_all()) == 2

    def test_readonly_override_set_JSON(helpers):
        new_instance = pytest.helpers.reconnect_swimlane(
            write_to_read_only=True)
        current_app = new_instance.apps.get(id=pytest.appid)
        fullRecord = current_app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        assert fullRecord.created == fullRecord.modified
        assert len(fullRecord.revisions.get_all()) == 1
        fullRecord['JSON'] = {'a': 123}
        fullRecord.save()
        assert fullRecord.created < fullRecord.modified
        assert len(fullRecord.revisions.get_all()) == 2
