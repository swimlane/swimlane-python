import pytest
from swimlane import exceptions


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


class TestRecordRestrictByUser:
    def test_record_has_access(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        tempRecord.add_restriction(
            pytest.swimlane_instance.users.get(id=pytest.newUser2['id']))
        new_instance = pytest.helpers.reconnect_swimlane(
            user=pytest.newUser2['userName'], password=pytest.newUser2['password'])
        currentapp = new_instance.apps.get(id=pytest.appid)
        openRecord = currentapp.records.get(id=pytest.fullRecord.id)
        record = currentapp.records.get(id=tempRecord.id)
        assert record['numeric'] == 123
        assert openRecord['numeric'] == 123

    def test_no_access_to_one_record(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        tempRecord.add_restriction(
            pytest.swimlane_instance.users.get(id=pytest.newUser2['id']))
        new_instance = pytest.helpers.reconnect_swimlane(
            user=pytest.newUser1['userName'], password=pytest.newUser1['password'])
        currentapp = new_instance.apps.get(id=pytest.appid)
        with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
            currentapp.records.get(id=tempRecord.id)
        assert str(excinfo.value) == 'RecordNotFound:3002: Bad Request for url: %s/api/app/%s/record/%s' % (
            pytest.helpers.url, pytest.appid, tempRecord.id)
        openRecord = currentapp.records.get(id=pytest.fullRecord.id)
        assert openRecord['numeric'] == 123

    def test_restriction_removed(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        tempRecord.add_restriction(
            pytest.swimlane_instance.users.get(id=pytest.newUser2['id']))
        restrictionsList = tempRecord.restrictions
        assert len(restrictionsList) == 1
        new_instance = pytest.helpers.reconnect_swimlane(
            user=pytest.newUser1['userName'], password=pytest.newUser1['password'])
        currentapp = new_instance.apps.get(id=pytest.appid)
        with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
            currentapp.records.get(id=tempRecord.id)
        assert str(excinfo.value) == 'RecordNotFound:3002: Bad Request for url: %s/api/app/%s/record/%s' % (
            pytest.helpers.url, pytest.appid, tempRecord.id)
        tempRecord.remove_restriction(
            pytest.swimlane_instance.users.get(id=pytest.newUser2['id']))
        assert len(tempRecord.restrictions) == 0
        assert restrictionsList != tempRecord.restrictions
        record = currentapp.records.get(id=tempRecord.id)
        assert record['numeric'] == 123

    def test_all_restriction_removed(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        tempRecord.add_restriction(pytest.swimlane_instance.users.get(
            id=pytest.newUser2['id']), pytest.swimlane_instance.users.get(id=pytest.newUser1['id']))
        restrictionsList = tempRecord.restrictions
        assert len(restrictionsList) == 2
        tempRecord.remove_restriction()
        assert len(tempRecord.restrictions) == 0
        assert restrictionsList != tempRecord.restrictions

    def test_restriction_remove_random_user(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        tempRecord.add_restriction(
            pytest.swimlane_instance.users.get(id=pytest.newUser2['id']))
        restrictionsList = tempRecord.restrictions
        assert len(restrictionsList) == 1
        with pytest.raises(ValueError) as excinfo:
            tempRecord.remove_restriction(
                pytest.swimlane_instance.users.get(id=pytest.newUser1['id']))
        assert str(excinfo.value) == 'UserGroup `%s` not in record `%s` restriction list' % (
            pytest.newUser1['name'], tempRecord.tracking_id)
        assert len(restrictionsList) == 1
        assert restrictionsList == tempRecord.restrictions

    def test_add_restriction_None_users(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        users = None
        with pytest.raises(TypeError) as excinfo:
            tempRecord.add_restriction(users)
        assert str(excinfo.value) == "Expected UserGroup, received `None` instead"
        assert len(tempRecord.restrictions) == 0

    def test_restriction_add_duplicate_user(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        tempRecord.add_restriction(
            pytest.swimlane_instance.users.get(id=pytest.newUser2['id']))
        restrictionsList = tempRecord.restrictions
        assert len(restrictionsList) == 1
        tempRecord.add_restriction(
            pytest.swimlane_instance.users.get(id=pytest.newUser2['id']))
        assert len(restrictionsList) == 1


class TestRecordRestrictByGroup:
    def test_add_restriction_Group(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        swimGroup = pytest.swimlane_instance.groups.get(
            id=pytest.newGroup1['id'])
        assert len(tempRecord.restrictions) == 0
        tempRecord.add_restriction(swimGroup)
        assert len(tempRecord.restrictions) == 1
        new_instance = pytest.helpers.reconnect_swimlane(
            user=pytest.newUser1['userName'], password=pytest.newUser1['password'])
        currentapp = new_instance.apps.get(id=pytest.appid)
        with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
            currentapp.records.get(id=tempRecord.id)
        assert str(excinfo.value) == 'RecordNotFound:3002: Bad Request for url: %s/api/app/%s/record/%s' % (
            pytest.helpers.url, pytest.appid, tempRecord.id)

    def test_remove_restriction_Group(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        swimGroup = pytest.swimlane_instance.groups.get(
            id=pytest.newGroup1['id'])
        tempRecord.add_restriction(swimGroup)
        assert len(tempRecord.restrictions) == 1
        new_instance = pytest.helpers.reconnect_swimlane(
            user=pytest.newUser1['userName'], password=pytest.newUser1['password'])
        currentapp = new_instance.apps.get(id=pytest.appid)
        with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
            currentapp.records.get(id=tempRecord.id)
        assert str(excinfo.value) == 'RecordNotFound:3002: Bad Request for url: %s/api/app/%s/record/%s' % (
            pytest.helpers.url, pytest.appid, tempRecord.id)
        tempRecord.remove_restriction(swimGroup)
        assert len(tempRecord.restrictions) == 0
        record = currentapp.records.get(id=tempRecord.id)
        assert record['numeric'] == 123

    def test_remove_all_restriction_Groups(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        swimGroup = pytest.swimlane_instance.groups.get(
            id=pytest.newGroup1['id'])
        tempRecord.add_restriction(swimGroup)
        restrictionsList = tempRecord.restrictions
        assert len(tempRecord.restrictions) == 1
        new_instance = pytest.helpers.reconnect_swimlane(
            user=pytest.newUser1['userName'], password=pytest.newUser1['password'])
        currentapp = new_instance.apps.get(id=pytest.appid)
        with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
            currentapp.records.get(id=tempRecord.id)
        assert str(excinfo.value) == 'RecordNotFound:3002: Bad Request for url: %s/api/app/%s/record/%s' % (
            pytest.helpers.url, pytest.appid, tempRecord.id)
        tempRecord.remove_restriction()
        record = currentapp.records.get(id=tempRecord.id)
        assert len(tempRecord.restrictions) == 0
        assert restrictionsList != tempRecord.restrictions
        assert record['numeric'] == 123

    def test_remove_random_restriction_Group(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        swimGroup = pytest.swimlane_instance.groups.get(
            id=pytest.newGroup1['id'])
        tempRecord.add_restriction(swimGroup)
        restrictionsList = tempRecord.restrictions
        assert len(restrictionsList) == 1
        swimGroup2 = pytest.swimlane_instance.groups.get(
            id=pytest.newGroup2['id'])
        with pytest.raises(ValueError) as excinfo:
            tempRecord.remove_restriction(swimGroup2)
        assert str(excinfo.value) == 'UserGroup `%s` not in record `%s` restriction list' % (
            pytest.newGroup2['name'], tempRecord.tracking_id)
        assert len(tempRecord.restrictions) == 1
        assert restrictionsList == tempRecord.restrictions

    def test_add_duplicate_Group(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        swimGroup = pytest.swimlane_instance.groups.get(
            id=pytest.newGroup1['id'])
        tempRecord.add_restriction(swimGroup)
        assert len(tempRecord.restrictions) == 1
        tempRecord.add_restriction(swimGroup)
        assert len(tempRecord.restrictions) == 1


class TestRecordRestrictByGroupAndUser:
    def test_add_restriction_Group_and_User(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        swimGroup = pytest.swimlane_instance.groups.get(
            id=pytest.newGroup1['id'])
        swimUser = pytest.swimlane_instance.users.get(id=pytest.newUser2['id'])
        assert len(tempRecord.restrictions) == 0
        tempRecord.add_restriction(swimGroup, swimUser)
        assert len(tempRecord.restrictions) == 2
        new_instance = pytest.helpers.reconnect_swimlane(
            user=pytest.newUser2['userName'], password=pytest.newUser2['password'])
        currentapp = new_instance.apps.get(id=pytest.appid)

        new_instance = pytest.helpers.reconnect_swimlane(
            user=pytest.newUser1['userName'], password=pytest.newUser1['password'])
        currentapp = new_instance.apps.get(id=pytest.appid)
        with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
            currentapp.records.get(id=tempRecord.id)
        assert str(excinfo.value) == 'RecordNotFound:3002: Bad Request for url: %s/api/app/%s/record/%s' % (
            pytest.helpers.url, pytest.appid, tempRecord.id)

    def test_add_restriction_Group_and_User_Seperate(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        swimGroup = pytest.swimlane_instance.groups.get(
            id=pytest.newGroup1['id'])
        swimUser = pytest.swimlane_instance.users.get(id=pytest.newUser2['id'])
        assert len(tempRecord.restrictions) == 0
        tempRecord.add_restriction(swimGroup)
        tempRecord.add_restriction(swimUser)
        assert len(tempRecord.restrictions) == 2

    def test_add_restriction_Group_and_User_Seperate_Saves(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        swimGroup = pytest.swimlane_instance.groups.get(
            id=pytest.newGroup1['id'])
        swimUser = pytest.swimlane_instance.users.get(id=pytest.newUser2['id'])
        assert len(tempRecord.restrictions) == 0
        tempRecord.add_restriction(swimGroup)
        assert len(tempRecord.restrictions) == 1
        tempRecord.add_restriction(swimUser)
        assert len(tempRecord.restrictions) == 2

    def test_add_restriction_Group_and_User_Remove_Group(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        swimGroup = pytest.swimlane_instance.groups.get(
            id=pytest.newGroup1['id'])
        swimUser = pytest.swimlane_instance.users.get(id=pytest.newUser2['id'])
        assert len(tempRecord.restrictions) == 0
        tempRecord.add_restriction(swimGroup, swimUser)
        assert len(tempRecord.restrictions) == 2
        tempRecord.remove_restriction(swimGroup)
        assert len(tempRecord.restrictions) == 1

    def test_add_restriction_Group_and_User_Remove_User(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        swimGroup = pytest.swimlane_instance.groups.get(
            id=pytest.newGroup1['id'])
        swimUser = pytest.swimlane_instance.users.get(id=pytest.newUser2['id'])
        assert len(tempRecord.restrictions) == 0
        tempRecord.add_restriction(swimGroup, swimUser)
        assert len(tempRecord.restrictions) == 2
        tempRecord.remove_restriction(swimUser)
        assert len(tempRecord.restrictions) == 1

    def test_add_restriction_Group_and_User_Remove_All(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        swimGroup = pytest.swimlane_instance.groups.get(
            id=pytest.newGroup1['id'])
        swimUser = pytest.swimlane_instance.users.get(id=pytest.newUser2['id'])
        assert len(tempRecord.restrictions) == 0
        tempRecord.add_restriction(swimGroup, swimUser)
        assert len(tempRecord.restrictions) == 2
        tempRecord.remove_restriction()
        assert len(tempRecord.restrictions) == 0


class TestRecordRestrictionMidWork:
    def test_restrict_user_while_working(helpers):
        tempRecord = pytest.app.records.create(
            **{'numeric': 123, 'Text': '2w3d'})
        # user gets record.
        new_instance = pytest.helpers.reconnect_swimlane(
            user=pytest.newUser1['userName'], password=pytest.newUser1['password'])
        currentapp = new_instance.apps.get(id=pytest.appid)
        record = currentapp.records.get(id=tempRecord.id)
        record.numeric = pytest.fake.random_int(min=0, max=9999)

        # admin restricts the record to not the user above
        tempRecord.add_restriction(
            pytest.swimlane_instance.users.get(id=pytest.newUser2['id']))

        # User who is not allowed tries to save record.
        with pytest.raises(exceptions.SwimlaneHTTP400Error) as excinfo:
            record.save()
        assert str(excinfo.value) == 'RecordNotFound:3002: Bad Request for url: %s/api/app/%s/record' % (
            pytest.helpers.url, pytest.appid)
