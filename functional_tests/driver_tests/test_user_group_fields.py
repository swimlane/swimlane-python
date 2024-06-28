import pytest
from swimlane import exceptions


@pytest.fixture(autouse=True, scope='module')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'user group fields'
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    pytest.testUsers = list(pytest.usersCreated.keys())
    pytest.testGroups = list(pytest.groupsCreated.keys())
    yield
    # teardown stuff
    helpers.cleanupData()


class TestRequiredUserGroupField:
    def test_required_field(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        assert theRecord["Required User/Groups"] == swimUser

    def test_required_field_not_set(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(**{"User/Groups": swimUser})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Required field "Required User/Groups" is not set' % pytest.app.acronym

    def test_required_field_not_set_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        theRecord["Required User/Groups"] = None
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord.save()
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Required field "Required User/Groups" is not set' % theRecord.tracking_id


class TestUserGroupField:
    def test_user_group_field(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "User/Groups": swimUser2})
        assert theRecord["User/Groups"].id == swimUser2.id

    def test_user_group_field_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        theRecord["User/Groups"] = swimUser2

    def test_user_group_field_bad_type_group(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name=pytest.testGroups[pytest.fake.random_int(0, len(pytest.testGroups)-1)])
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "User/Groups": swimGroup})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Group "%s" is not a valid selection for field "User/Groups"' % (
            pytest.app.acronym, swimGroup.name)

    def test_user_group_field_on_save_bad_type_group(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name=pytest.testGroups[pytest.fake.random_int(0, len(pytest.testGroups)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["User/Groups"] = swimGroup
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Group "%s" is not a valid selection for field "User/Groups"' % (
            theRecord.tracking_id, swimGroup.name)


class TestGroupsOnlyField:
    def test_groups_only_field(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name=pytest.testGroups[pytest.fake.random_int(0, len(pytest.testGroups)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "Groups Only": swimGroup})
        assert theRecord["Groups Only"] == swimGroup

    def test_groups_only_field_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name=pytest.testGroups[pytest.fake.random_int(0, len(pytest.testGroups)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        theRecord["Groups Only"] = swimGroup

    def test_groups_only_field_bad_type_user(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Groups Only": swimUser2})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: User "%s" is not a valid selection for field "Groups Only"' % (
            pytest.app.acronym, swimUser2.username)

    def test_groups_only_field_on_save_bad_type_user(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Groups Only"] = swimUser2
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: User "%s" is not a valid selection for field "Groups Only"' % (
            theRecord.tracking_id, swimUser2.username)


class TestReadOnlyUserGroupsField:
    def test_read_only_user_groups_field(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Read-only User/Groups": swimUser2})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Cannot set readonly field "Read-only User/Groups"' % pytest.app.acronym

    def test_read_only_user_groups_field_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Read-only User/Groups"] = swimUser2
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Cannot set readonly field "Read-only User/Groups"' % theRecord.tracking_id


class TestCreatedByField:
    def test_created_by_field_value(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        assert theRecord["Created by"] == swimUser

    def test_created_by_field(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        with pytest.raises(ValueError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Created by": swimUser2})
        assert str(excinfo.value) == 'Input type "createdBy" is not editable'

    def test_created_by_field_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(ValueError) as excinfo:
            theRecord["Created by"] = swimUser2
        assert str(excinfo.value) == 'Input type "createdBy" is not editable'


class TestLastUpdatedByField:
    def test_last_updated_by_field_value(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        assert theRecord["Last updated by"] == swimUser

    def test_last_updated_by_field(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        with pytest.raises(ValueError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Last updated by": swimUser2})
        assert str(excinfo.value) == 'Input type "lastUpdatedBy" is not editable'


    def test_last_updated_by_field_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(ValueError) as excinfo:    
            theRecord["Last updated by"] = swimUser2
        assert str(excinfo.value) == 'Input type "lastUpdatedBy" is not editable'


class TestAllUsersAndGroupsField:
    def test_all_users_and_groups_field_user(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "All Users and Groups": swimUser2})
        assert theRecord["All Users and Groups"].id == swimUser2.id

    def test_all_users_and_groups_field_group(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name=pytest.testGroups[pytest.fake.random_int(0, len(pytest.testGroups)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "All Users and Groups": swimGroup})
        assert theRecord["All Users and Groups"] == swimGroup

    def test_all_users_and_groups_field_user_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        theRecord["All Users and Groups"] = swimUser2
        theRecord.save()

    def test_all_users_and_groups_field_group_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name=pytest.testGroups[pytest.fake.random_int(0, len(pytest.testGroups)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        theRecord["All Users and Groups"] = swimGroup
        theRecord.save()

    def test_all_users_and_groups_field_on_save_bad_value_type(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name=pytest.testGroups[pytest.fake.random_int(0, len(pytest.testGroups)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["All Users and Groups"] = {"name": swimGroup}
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Field "All Users and Groups" expects one of \'UserGroup\', got "dict" instead' % theRecord.tracking_id


class TestSelectedGroupsField:
    def test_selected_groups_field(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(name="PYTHON-groupTwo")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "Selected Groups": swimGroup})
        assert theRecord["Selected Groups"] == swimGroup

    def test_selected_groups_field_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(name="PYTHON-groupOne")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        theRecord["Selected Groups"] = swimGroup
        theRecord.save()

    def test_selected_groups_field_wrong_group(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name="PYTHON-groupFour")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Selected Groups": swimGroup})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Group "%s" is not a valid selection for field "Selected Groups"' % (
            pytest.app.acronym, swimGroup.name)

    def test_selected_groups_field_wrong_group_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name="PYTHON-groupThree")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Selected Groups"] = swimGroup
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Group "%s" is not a valid selection for field "Selected Groups"' % (
            theRecord.tracking_id, swimGroup.name)

    def test_selected_groups_field_bad_type_user(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Selected Groups": swimUser2})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: User "%s" is not a valid selection for field "Selected Groups"' % (
            pytest.app.acronym, swimUser2.username)

    def test_selected_groups_field_on_save_bad_type_user(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Selected Groups"] = swimUser2
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: User "%s" is not a valid selection for field "Selected Groups"' % (
            theRecord.tracking_id, swimUser2.username)


class TestSelectedUsersField:
    def test_selected_users_field(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userOne")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "Selected Users": swimUser2})
        assert theRecord["Selected Users"].id == swimUser2.id

    def test_selected_users_field_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userFour")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        theRecord["Selected Users"] = swimUser2
        theRecord.save()

    def test_selected_users_field_wrong_user(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userTwo")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Selected Users": swimUser2})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: User "%s" is not a valid selection for field "Selected Users"' % (
            pytest.app.acronym, swimUser2.username)

    def test_selected_users_field_wrong_user_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userThree")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Selected Users"] = swimUser2
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: User "%s" is not a valid selection for field "Selected Users"' % (
            theRecord.tracking_id, swimUser2.username)

    def test_selected_users_field_bad_type_group(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name=pytest.testGroups[pytest.fake.random_int(0, len(pytest.testGroups)-1)])
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Selected Users": swimGroup})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Group "%s" is not a valid selection for field "Selected Users"' % (
            pytest.app.acronym, swimGroup.name)

    def test_selected_users_field_on_save_bad_type_group(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name=pytest.testGroups[pytest.fake.random_int(0, len(pytest.testGroups)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Selected Users"] = swimGroup
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Group "%s" is not a valid selection for field "Selected Users"' % (
            theRecord.tracking_id, swimGroup.name)


class TestSubgroupsOfGroupField:
    def test_sub_groups_of_group_field(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(name="PYTHON-groupOne")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "Sub-groups of Group": swimGroup})
        assert theRecord["Sub-groups of Group"] == swimGroup

    def test_sub_groups_of_group_field_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(name="PYTHON-groupTwo")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        theRecord["Sub-groups of Group"] = swimGroup
        theRecord.save()

    def test_sub_groups_of_group_field_parent_group(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name="PYTHON-groupCombo")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Sub-groups of Group": swimGroup})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Group "%s" is not a valid selection for field "Sub-groups of Group"' % (
            pytest.app.acronym, swimGroup.name)

    def test_sub_groups_of_group_field_parent_group_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name="PYTHON-groupCombo")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Sub-groups of Group"] = swimGroup
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Group "%s" is not a valid selection for field "Sub-groups of Group"' % (
            theRecord.tracking_id, swimGroup.name)

    def test_sub_groups_of_group_field_other_group(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name="PYTHON-groupFour")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Sub-groups of Group": swimGroup})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Group "%s" is not a valid selection for field "Sub-groups of Group"' % (
            pytest.app.acronym, swimGroup.name)

    def test_sub_groups_of_group_field_other_group_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name="PYTHON-groupFour")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Sub-groups of Group"] = swimGroup
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Group "%s" is not a valid selection for field "Sub-groups of Group"' % (
            theRecord.tracking_id, swimGroup.name)

    def test_sub_groups_of_group_field_user(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Sub-groups of Group": swimUser2})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: User "%s" is not a valid selection for field "Sub-groups of Group"' % (
            pytest.app.acronym, swimUser2.username)

    def test_sub_groups_of_group_field_user_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Sub-groups of Group"] = swimUser2
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: User "%s" is not a valid selection for field "Sub-groups of Group"' % (
            theRecord.tracking_id, swimUser2.username)


class TestUsersMembersOfGroupField:
    @pytest.mark.xfail(reason="SPT-6355: Says the user who belongs to the group is not a valid selection.")
    def test_users_members_of_group_field(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userOne")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "Users Members of Group": swimUser2})
        assert theRecord["Users Members of Group"] == swimUser2

    @pytest.mark.xfail(reason="SPT-6355: Says the user who belongs to the group is not a valid selection.")
    def test_users_members_of_group_field_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userTwo")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        theRecord["Users Members of Group"] = swimUser2
        theRecord.save()

    def test_users_members_of_group_field_user_not_member(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userFour")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Users Members of Group": swimUser2})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: User "%s" is not a valid selection for field "Users Members of Group"' % (
            pytest.app.acronym, swimUser2.username)

    def test_users_members_of_group_field_not_member_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userFour")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Users Members of Group"] = swimUser2
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: User "%s" is not a valid selection for field "Users Members of Group"' % (
            theRecord.tracking_id, swimUser2.username)

    def test_users_members_of_group_field_user_parent_group(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(name="PYTHON-groupTwo")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Users Members of Group": swimGroup})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Group "%s" is not a valid selection for field "Users Members of Group"' % (pytest.app.acronym, swimGroup.name)

    def test_users_members_of_group_field_parent_group_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(name="PYTHON-groupTwo")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Users Members of Group"] = swimGroup
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Group "%s" is not a valid selection for field "Users Members of Group"' % (
            theRecord.tracking_id, swimGroup.name)


class TestMultiSelectUsersField:
    def test_multi_select_users_field(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "Multi-select User/Groups": [swimUser2]})
        assert len(theRecord["Multi-select User/Groups"]) == 1
        for member in theRecord["Multi-select User/Groups"]:
            assert member.id == swimUser2.id

    def test_multi_select_users_field_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        theRecord["Multi-select User/Groups"] = [swimUser2]
        theRecord.save()

    # Should we handle this or say it has to be a list/array?
    def test_multi_select_users_field_single_user(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        with pytest.raises(TypeError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Multi-select User/Groups": swimUser2})
        assert str(excinfo.value) == '\'User\' object is not iterable'

    # Should we handle this or say it has to be a list/array?
    def test_multi_select_users_field_single_user_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(TypeError) as excinfo:
            theRecord["Multi-select User/Groups"] = swimUser2
        assert str(excinfo.value) == '\'User\' object is not iterable'

    def test_multi_select_users_field_group(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name=pytest.testGroups[pytest.fake.random_int(0, len(pytest.testGroups)-1)])
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Multi-select User/Groups": [swimGroup]})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Group "%s" is not a valid selection for field "Multi-select User/Groups"' % (pytest.app.acronym, swimGroup.name)

    def test_multi_select_users_field_group_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name=pytest.testGroups[pytest.fake.random_int(0, len(pytest.testGroups)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Multi-select User/Groups"] = [swimGroup]
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Group "%s" is not a valid selection for field "Multi-select User/Groups"' % (
            theRecord.tracking_id, swimGroup.name)

    def test_multi_select_users_field_mix_users_groups(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name=pytest.testGroups[pytest.fake.random_int(0, len(pytest.testGroups)-1)])
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Multi-select User/Groups": [swimUser2, swimGroup]})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Group "%s" is not a valid selection for field "Multi-select User/Groups"' % (pytest.app.acronym, swimGroup.name)

    def test_multi_select_users_field_mix_users_groups_on_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        swimGroup = pytest.swimlane_instance.groups.get(
            name=pytest.testGroups[pytest.fake.random_int(0, len(pytest.testGroups)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Multi-select User/Groups"] = [swimUser2, swimGroup]
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Group "%s" is not a valid selection for field "Multi-select User/Groups"' % (
            theRecord.tracking_id, swimGroup.name)

    @pytest.mark.xfail(reason="SPT-6354: This works for the adminuser, but not the others..")
    def test_multi_select_users_field_deselect_user(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "Multi-select User/Groups": [swimUser, swimUser2]})
        theRecord["Multi-select User/Groups"].deselect(swimUser2)
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord["Multi-select User/Groups"]) == 1
        assert updatedRecord["Multi-select User/Groups"][0].id == swimUser.id

    def test_multi_select_users_field_deselect_other_user(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userOne")
        swimUser3 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userTwo")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "Multi-select User/Groups": [swimUser, swimUser2]})
        with pytest.raises(KeyError) as excinfo:
            theRecord["Multi-select User/Groups"].deselect(swimUser3)
        assert str(excinfo.value) == '<User: %s>' % swimUser3.username
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord["Multi-select User/Groups"]) == 2
        userIds = [updatedRecord["Multi-select User/Groups"][1].id,
                   updatedRecord["Multi-select User/Groups"][0].id]
        assert swimUser.id in userIds
        assert swimUser2.id in userIds

    def test_multi_select_users_field_select_user(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userOne")
        swimUser3 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userTwo")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "Multi-select User/Groups": [swimUser, swimUser2]})
        theRecord["Multi-select User/Groups"].select(swimUser3)
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord["Multi-select User/Groups"]) == 3
        userIds = [updatedRecord["Multi-select User/Groups"][1].id,
                   updatedRecord["Multi-select User/Groups"][0].id, updatedRecord["Multi-select User/Groups"][2].id]
        assert swimUser3.id in userIds
        assert swimUser2.id in userIds
        assert swimUser.id in userIds

    def test_multi_select_users_field_select_existing_user(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userOne")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "Multi-select User/Groups": [swimUser, swimUser2]})
        theRecord["Multi-select User/Groups"].select(swimUser2)
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord["Multi-select User/Groups"]) == 2
        userIds = [updatedRecord["Multi-select User/Groups"][1].id,
                   updatedRecord["Multi-select User/Groups"][0].id]
        assert swimUser.id in userIds
        assert swimUser2.id in userIds

    def test_multi_select_users_field_select_group(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name=pytest.testUsers[pytest.fake.random_int(0, len(pytest.testUsers)-1)])
        swimGroup = pytest.swimlane_instance.groups.get(
            name=pytest.testGroups[pytest.fake.random_int(0, len(pytest.testGroups)-1)])
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "Multi-select User/Groups": [swimUser, swimUser2]})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Multi-select User/Groups"].select(swimGroup)
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Group "%s" is not a valid selection for field "Multi-select User/Groups"' % (
            theRecord.tracking_id, swimGroup.name)
        theRecord.save()
        updatedRecord = pytest.app.records.get(id=theRecord.id)
        assert len(updatedRecord["Multi-select User/Groups"]) == 2
        userIds = [updatedRecord["Multi-select User/Groups"][1].id,
                   updatedRecord["Multi-select User/Groups"][0].id]
        assert swimUser.id in userIds
        assert swimUser2.id in userIds


class TestMultiSelectSpecificUsersAndGroupsField:
    def test_multi_select_specific_users_groups_field_user_create(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userOne")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "Multi-select Specific Users and Groups": [swimUser2]})
        assert len(theRecord["Multi-select Specific Users and Groups"]) == 1
        for member in theRecord["Multi-select Specific Users and Groups"]:
            assert member.id == swimUser2.id

    def test_multi_select_specific_users_groups_field_group_create(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(name="PYTHON-groupTwo")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "Multi-select Specific Users and Groups": [swimGroup]})
        assert len(theRecord["Multi-select Specific Users and Groups"]) == 1
        for member in theRecord["Multi-select Specific Users and Groups"]:
            assert member.id == swimGroup.id

    def test_multi_select_specific_users_groups_field_user_and_group_create(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userOne")
        swimGroup = pytest.swimlane_instance.groups.get(name="PYTHON-groupTwo")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "Multi-select Specific Users and Groups": [swimUser2, swimGroup]})
        assert len(theRecord["Multi-select Specific Users and Groups"]) == 2
        for member in theRecord["Multi-select Specific Users and Groups"]:
            assert member.id in [swimUser2.id, swimGroup.id]

    def test_multi_select_specific_users_groups_field_user_and_group_invalid_user_create(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userTwo")
        swimGroup = pytest.swimlane_instance.groups.get(name="PYTHON-groupTwo")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Multi-select Specific Users and Groups": [swimGroup, swimUser2]})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: User "%s" is not a valid selection for field "Multi-select Specific Users and Groups"' % (
            pytest.app.acronym, swimUser2.username)

    def test_multi_select_specific_users_groups_field_user_and_group_invalid_group_create(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userOne")
        swimGroup = pytest.swimlane_instance.groups.get(
            name="PYTHON-groupThree")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Multi-select Specific Users and Groups": [swimGroup, swimUser2]})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Group "%s" is not a valid selection for field "Multi-select Specific Users and Groups"' % (pytest.app.acronym, swimGroup.name)

    def test_multi_select_specific_users_groups_field_invalid_group_create(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name="PYTHON-groupFour")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Multi-select Specific Users and Groups": [swimGroup]})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Group "%s" is not a valid selection for field "Multi-select Specific Users and Groups"' % (pytest.app.acronym, swimGroup.name)

    def test_multi_select_specific_users_groups_field_invalid_group_subgroup_create(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name="PYTHON-groupThree")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Multi-select Specific Users and Groups": [swimGroup]})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Group "%s" is not a valid selection for field "Multi-select Specific Users and Groups"' % (pytest.app.acronym, swimGroup.name)

    def test_multi_select_specific_users_groups_field_invalid_user_create(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userTwo")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Multi-select Specific Users and Groups": [swimUser2]})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: User "%s" is not a valid selection for field "Multi-select Specific Users and Groups"' % (
            pytest.app.acronym, swimUser2.username)

    def test_multi_select_specific_users_groups_field_invalid_user_group_member_create(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userThree")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Multi-select Specific Users and Groups": [swimUser2]})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: User "%s" is not a valid selection for field "Multi-select Specific Users and Groups"' % (
            pytest.app.acronym, swimUser2.username)

    def test_multi_select_specific_users_groups_field_user_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userOne")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        theRecord["Multi-select Specific Users and Groups"] = [swimUser2]
        theRecord.save()

    def test_multi_select_specific_users_groups_field_group_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(name="PYTHON-groupTwo")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        theRecord["Multi-select Specific Users and Groups"] = [swimGroup]
        theRecord.save()

    def test_multi_select_specific_users_groups_field_user_and_group_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userOne")
        swimGroup = pytest.swimlane_instance.groups.get(name="PYTHON-groupTwo")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        theRecord["Multi-select Specific Users and Groups"] = [swimUser2, swimGroup]
        theRecord.save()

    def test_multi_select_specific_users_groups_field_invalid_group_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name="PYTHON-groupFour")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Multi-select Specific Users and Groups"] = [swimGroup]
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Group "%s" is not a valid selection for field "Multi-select Specific Users and Groups"' % (
            theRecord.tracking_id, swimGroup.name)

    def test_multi_select_specific_users_groups_field_invalid_group_subgroup_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name="PYTHON-groupThree")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Multi-select Specific Users and Groups"] = [swimGroup]
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Group "%s" is not a valid selection for field "Multi-select Specific Users and Groups"' % (
            theRecord.tracking_id, swimGroup.name)

    def test_multi_select_specific_users_groups_field_invalid_user_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userTwo")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Multi-select Specific Users and Groups"] = [swimUser2]
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: User "%s" is not a valid selection for field "Multi-select Specific Users and Groups"' % (
            theRecord.tracking_id, swimUser2.username)

    def test_multi_select_specific_users_groups_field_invalid_user_group_member_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userThree")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Multi-select Specific Users and Groups"] = [swimUser2]
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: User "%s" is not a valid selection for field "Multi-select Specific Users and Groups"' % (
            theRecord.tracking_id, swimUser2.username)


class TestSelectSpecificUsersAndGroupsField:
    def test_select_specific_users_groups_field_user_create(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userOne")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "Specific Users and Groups": swimUser2})
        assert theRecord["Specific Users and Groups"].id == swimUser2.id

    def test_select_specific_users_groups_field_group_create(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(name="PYTHON-groupTwo")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser, "Specific Users and Groups": swimGroup})
        assert theRecord["Specific Users and Groups"] == swimGroup

    def test_select_specific_users_groups_field_invalid_group_create(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name="PYTHON-groupFour")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Specific Users and Groups": swimGroup})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Group "%s" is not a valid selection for field "Specific Users and Groups"' % (pytest.app.acronym, swimGroup.name)

    def test_select_specific_users_groups_field_invalid_group_subgroup_create(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name="PYTHON-groupThree")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Specific Users and Groups": swimGroup})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Group "%s" is not a valid selection for field "Specific Users and Groups"' % (pytest.app.acronym, swimGroup.name)

    def test_select_specific_users_groups_field_invalid_user_create(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userTwo")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Specific Users and Groups": swimUser2})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: User "%s" is not a valid selection for field "Specific Users and Groups"' % (
            pytest.app.acronym, swimUser2.username)

    def test_select_specific_users_groups_field_invalid_user_group_member_create(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userThree")
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required User/Groups": swimUser, "Specific Users and Groups": swimUser2})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: User "%s" is not a valid selection for field "Specific Users and Groups"' % (
            pytest.app.acronym, swimUser2.username)

    def test_select_specific_users_groups_field_user_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userOne")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        theRecord["Specific Users and Groups"] = swimUser2
        theRecord.save()

    def test_select_specific_users_groups_field_group_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(name="PYTHON-groupTwo")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        theRecord["Specific Users and Groups"] = swimGroup
        theRecord.save()

    def test_select_specific_users_groups_field_invalid_group_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name="PYTHON-groupFour")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Specific Users and Groups"] = swimGroup
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Group "%s" is not a valid selection for field "Specific Users and Groups"' % (
            theRecord.tracking_id, swimGroup.name)

    def test_select_specific_users_groups_field_invalid_group_subgroup_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimGroup = pytest.swimlane_instance.groups.get(
            name="PYTHON-groupThree")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Specific Users and Groups"] = swimGroup
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Group "%s" is not a valid selection for field "Specific Users and Groups"' % (
            theRecord.tracking_id, swimGroup.name)

    def test_select_specific_users_groups_field_invalid_user_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userTwo")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Specific Users and Groups"] = swimUser2
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: User "%s" is not a valid selection for field "Specific Users and Groups"' % (
            theRecord.tracking_id, swimUser2.username)

    def test_select_specific_users_groups_field_invalid_user_group_member_save(helpers):
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        swimUser2 = pytest.swimlane_instance.users.get(
            display_name="PYTHON-userThree")
        theRecord = pytest.app.records.create(
            **{"Required User/Groups": swimUser})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Specific Users and Groups"] = swimUser2
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: User "%s" is not a valid selection for field "Specific Users and Groups"' % (
            theRecord.tracking_id, swimUser2.username)
