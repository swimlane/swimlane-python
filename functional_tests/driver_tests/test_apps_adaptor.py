import pytest


@pytest.fixture(autouse=True, scope='module')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'Email Collection'
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.py_ver_uni_str = helpers.py_ver_uni_str
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    yield
    # teardown stuff
    helpers.cleanupData()


class TestAppsAdaptor:
    def test_list(helpers):
        swimAppList = pytest.swimlane_instance.apps.list()
        assert len(swimAppList) >= 1

    def test_get_by_id(helpers):
        swimApp = pytest.swimlane_instance.apps.get(id=pytest.app.id)
        assert swimApp == pytest.app

    def test_get_by_name(helpers):
        swimApp = pytest.swimlane_instance.apps.get(name=pytest.app.name)
        assert swimApp == pytest.app

    def test_get_by_fake_id(helpers):
        randomID = pytest.fake.random_int()
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.apps.get(id=randomID)
        assert str(excinfo.value) == 'No app with id "%s"' % randomID

    @pytest.mark.xfail(reason="SPT-5944: Testing for randomID as empty does not give formal response (attributeError)")
    def test_get_by_empty_id(helpers):
        randomID = ""
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.apps.get(id=randomID)
        assert str(excinfo.value) == 'No app with id "%s"' % randomID

    @pytest.mark.xfail(reason="SPT-5944: Testing for randomName as empty should check on value is empty")
    def test_get_by_empty_name(helpers):
        randomName = ""
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.apps.get(name=randomName)
        assert str(excinfo.value) == 'No app with name "%s"' % randomName

    def test_get_by_fake_name(helpers):
        randomName = pytest.fake.sentence()
        with pytest.raises(ValueError) as excinfo:
            pytest.swimlane_instance.apps.get(name=randomName)
        assert str(excinfo.value) == 'No app with name "%s"' % randomName

    def test_get_by_id_and_name(helpers):
        with pytest.raises(TypeError) as excinfo:
            pytest.swimlane_instance.apps.get(
                name=pytest.app.name, id=pytest.app.id)
        assert str(excinfo.value) == "Must provide only one of id, name as keyword argument. Received {{'id': {}, 'name': {}}}".format(
            pytest.py_ver_uni_str(pytest.app.id), pytest.py_ver_uni_str(pytest.app.name))
