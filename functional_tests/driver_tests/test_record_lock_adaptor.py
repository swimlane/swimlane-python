import pytest


@pytest.fixture(autouse=True, scope='module')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'basic app'
    pytest.helpers = helpers
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.waitOnJobByID = helpers.waitOnJobByID
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    pytest.newRole = pytest.helpers.createRole(
        sections=['Application', 'Report', 'Workspace', 'Dashboard', 'Applet'])
    userRoles = [{
        "id": pytest.newRole['id'],
        "name": pytest.newRole['name'],
        "disabled": False
    }]
    pytest.newGroup1 = pytest.helpers.createGroup()
    pytest.newGroup2 = pytest.helpers.createGroup()
    pytest.newUser1 = pytest.helpers.createUser(roles=userRoles)
    pytest.newUser2 = pytest.helpers.createUser(roles=userRoles)
    pytest.fullRecord = pytest.app.records.create(
        **{'numeric': 123, 'Text': '2w3d'})
    yield
    # teardown stuff
    helpers.cleanupData()


class TestLockRecord:
    def test_lock_record(self, helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        tempRecord.lock()
        assert(tempRecord.locked is True)
        assert(tempRecord.locking_user is not None)
        assert(tempRecord.locked_date is not None)
        assert(tempRecord.locking_user.name == helpers.userName)


class TestUnlockRecord:
    def test_unlock_record(self, helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        tempRecord.lock()
        assert(tempRecord.locked is True)
        tempRecord.unlock()
        assert(tempRecord.locking_user is None)
        assert(tempRecord.locked_date is None)
        assert(tempRecord.locking_user is None)
