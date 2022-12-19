import pytest


@pytest.fixture(autouse=True, scope='session')
def my_fixture(helpers):
    # setup stuff
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.py_ver_uni_str = helpers.py_ver_uni_str
    pytest.tempUser = helpers.createUser()
    pytest.tempGroup = helpers.createGroup()
    yield
    # teardown stuff


class TestUserAdaptor:
    def test_users_list(helpers):
        swimUsers = pytest.swimlane_instance.users.list()
        usersList = list(swimUsers)
        usersList2 = [str(x) for x in swimUsers]
        assert "admin" in usersList2
        assert pytest.tempUser['userName'] in usersList2
        assert len(usersList) >= 2

    def test_users_list_count_limit(helpers):
        maxUsers = 1
        swimUsers = pytest.swimlane_instance.users.list(limit=maxUsers)
        assert len(swimUsers) == maxUsers

    def test_users_list_count_limit_not_valid_string(helpers):
        stringLimit = 'Hello'
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.users.list(limit=stringLimit)
        assert str(excinfo.value) == 'Limit should be a positive whole number greater than 0'

    def test_users_list_count_limit_not_valid_empty_string(helpers):
        stringLimit = ''
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.users.list(limit=stringLimit)
        assert str(excinfo.value) == 'Limit should be a positive whole number greater than 0'

    def test_users_list_count_limit_not_valid_float(helpers):
        floatLimit = 5.5
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.users.list(limit=floatLimit)
        assert str(excinfo.value) == 'Limit should be a positive whole number greater than 0'

    def test_users_list_count_limit_not_valid_negative_int(helpers):
        negativeIntLimit = -3
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.users.list(limit=negativeIntLimit)
        assert str(excinfo.value) == 'Limit should be a positive whole number greater than 0'

    def test_users_list_count_limit_not_valid_zero(helpers):
        zeroLimit = 0
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.users.list(limit=zeroLimit)
        assert str(excinfo.value) == 'Limit should be a positive whole number greater than 0'

    def test_users_get_by_id(helpers):
        swimUser = pytest.swimlane_instance.users.get(id=pytest.tempUser['id'])
        assert swimUser.for_json()["name"] == pytest.tempUser['userName']

    def test_users_get_by_invalid_id(helpers):
        randomID = '123adv12312'
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.users.get(id=randomID)
        assert str(excinfo.value) == 'Unable to find user with ID "%s"' % randomID

    @pytest.mark.xfail(reason="SPT-6030: Testing for randomID as empty does not give formal response (attributeError)")
    def test_users_get_by_empty_id(helpers):
        emptyID = ''
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.users.get(id=emptyID)
        assert str(excinfo.value) == 'Unable to find user with ID "%s"' % emptyID

    @pytest.mark.xfail(reason="SPT-6030: Testing for display_Name as None givesValueError: Unable to find user with ID \"None\"")
    def test_users_get_by_null_id(helpers):
        noneID = None
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.users.get(id=noneID)
        assert str(excinfo.value) == 'Unable to find user with ID "%s"' % noneID

    def test_users_get_by_display_name(helpers):
        swimUser = pytest.swimlane_instance.users.get(
            display_name=pytest.tempUser['displayName'])
        assert swimUser.for_json()["id"] == pytest.tempUser['id']

    def test_users_get_by_invalid_display_name(helpers):
        randomDisplayName = "really random display name"
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.users.get(display_name=randomDisplayName)
        assert str(
            excinfo.value) == 'Unable to find user with display name "%s"' % randomDisplayName

    @pytest.mark.xfail(reason="SPT-6030: Testing for display_Name as an empty string should fail")
    def test_users_get_by_empty_display_name(helpers):
        emptyDisplayName = ""
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.users.get(display_name=emptyDisplayName)
        assert str(
            excinfo.value) == 'Unable to find user with display name "%s"' % emptyDisplayName

    @pytest.mark.xfail(reason="SPT-6030: Testing for display_Name as None gives  TypeError: argument of type 'NoneType' is not iterable")
    def test_users_get_by_null_display_name(helpers):
        randomDisplayName = None
        # we should be catchiong an exception for the display_name being an invalid type.
        pytest.swimlane_instance.users.get(display_name=randomDisplayName)

    def test_users_get_no_params(helpers):
        with pytest.raises(TypeError) as excinfo:
            pytest.swimlane_instance.users.get()
        assert str(
            excinfo.value) == 'Must provide one of id, display_name as keyword argument'

    def test_users_get_invalid_param(helpers):
        with pytest.raises(TypeError) as excinfo:
            pytest.swimlane_instance.users.get(garbage=pytest.tempUser['id'])
        assert str(excinfo.value) == "Unexpected arguments: {{'garbage': {}}}".format(
            pytest.py_ver_uni_str(pytest.tempUser['id']))


class TestGroupAdaptor:
    def test_groups_list(helpers):
        swimGroups = pytest.swimlane_instance.groups.list()
        groupsList = list(swimGroups)
        groupsList2 = [str(x) for x in swimGroups]
        assert "Everyone" in groupsList2
        assert pytest.tempGroup['name'] in groupsList2
        assert len(groupsList) >= 2

    def test_groups_list_count_limit(helpers):
        maxGroups = 1
        swimGroups = pytest.swimlane_instance.groups.list(limit=maxGroups)
        assert len(swimGroups) == maxGroups

    def test_groups_list_count_limit_not_valid_string(helpers):
        stringLimit = 'Hello'
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.groups.list(limit=stringLimit)
        assert str(excinfo.value) == 'Limit should be a positive whole number greater than 0'

    def test_groups_list_count_limit_not_valid_empty_string(helpers):
        stringLimit = ''
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.groups.list(limit=stringLimit)
        assert str(excinfo.value) == 'Limit should be a positive whole number greater than 0'

    def test_groups_list_count_limit_not_valid_float(helpers):
        floatLimit = 5.5
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.groups.list(limit=floatLimit)
        assert str(excinfo.value) == 'Limit should be a positive whole number greater than 0'

    def test_groups_list_count_limit_not_valid_zero(helpers):
        zeroLimit = 0
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.groups.list(limit=zeroLimit)
        assert str(excinfo.value) == 'Limit should be a positive whole number greater than 0'

    def test_groups_list_count_limit_not_valid_negative_int(helpers):
        negativeIntLimit = -3
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.groups.list(limit=negativeIntLimit)
        assert str(excinfo.value) == 'Limit should be a positive whole number greater than 0'

    def test_grouprs_get_by_id(helpers):
        swimGroup = pytest.swimlane_instance.groups.get(
            id=pytest.tempGroup['id'])
        assert swimGroup.for_json()["name"] == pytest.tempGroup['name']

    @pytest.mark.xfail(reason="SPT-6030: Testing for randomID as empty does not give formal response (attributeError)")
    def test_groups_get_by_empty_id(helpers):
        emptyID = ''
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.groups.get(id=emptyID)
        assert str(excinfo.value) == 'Unable to find group with ID "%s"' % emptyID

    @pytest.mark.xfail(reason="SPT-6030: Testing for ID as None givesValueError: Unable to find group with ID \"None\"")
    def test_groups_get_by_null_id(helpers):
        noneID = None
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.groups.get(id=noneID)
        assert str(excinfo.value) == 'Unable to find group with ID "%s"' % noneID

    def test_groups_get_by_name(helpers):
        swimGroup = pytest.swimlane_instance.groups.get(
            name=pytest.tempGroup['name'])
        assert swimGroup.for_json()["id"] == pytest.tempGroup['id']

    def test_groups_get_by_invalid_name(helpers):
        randomName = "really random group name"
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.groups.get(name=randomName)
        assert str(
            excinfo.value) == 'Unable to find group with name "%s"' % randomName

    @pytest.mark.xfail(reason="SPT-6030: Testing for name as empty string does error out")
    def test_groups_get_by_empty_name(helpers):
        emptyName = ""
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.groups.get(name=emptyName)
        assert str(
            excinfo.value) == 'Unable to find group with name "%s"' % emptyName

    @pytest.mark.xfail(reason="SPT-6030: Testing for Name as None gives  TypeError: argument of type 'NoneType' is not iterable")
    def test_groups_get_by_null_name(helpers):
        noneName = None
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.groups.get(name=noneName)
        assert str(
            excinfo.value) == 'Unable to find group with name "%s"' % noneName

    def test_groups_get_no_params(helpers):
        with pytest.raises(TypeError) as excinfo:
            pytest.swimlane_instance.groups.get()
        assert str(
            excinfo.value) == 'Must provide one of id, name as keyword argument'

    def test_groups_get_invalid_param(helpers):
        with pytest.raises(TypeError) as excinfo:
            pytest.swimlane_instance.groups.get(garbage=pytest.tempGroup['id'])
        assert str(excinfo.value) == "Unexpected arguments: {{'garbage': {}}}".format(
            pytest.py_ver_uni_str(pytest.tempGroup['id']))
