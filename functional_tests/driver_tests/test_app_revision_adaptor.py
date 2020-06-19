import pytest


@pytest.fixture(autouse=True, scope='module')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'Email Collection'
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.py_ver_no_json = helpers.py_ver_no_json
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    pytest.app2 = helpers.updateApp(pytest.appid)
    pytest.app3 = helpers.updateApp(pytest.appid)
    pytest.finalApp = helpers.updateApp(pytest.appid)
    yield
    # teardown stuff
    helpers.cleanupData()


class TestAppRevisionAdaptor:
    def test_app_get_all(helpers):
        theapp = pytest.swimlane_instance.apps.get(id=pytest.appid)
        revisionList = theapp.revisions.get_all()
        assert len(revisionList) == 4

    def test_app_get_specific_revision(helpers):
        theapp = pytest.swimlane_instance.apps.get(id=pytest.appid)
        app_rev = theapp.revisions.get(2)
        assert app_rev.revision_number == 2
        assert app_rev.version.description == pytest.app2.description

    def test_app_get_negative_number_revision(helpers):
        theapp = pytest.swimlane_instance.apps.get(id=pytest.appid)
        with pytest.raises(ValueError) as excinfo:
            theapp.revisions.get(-2)
        assert str(excinfo.value) == pytest.py_ver_no_json()

    def test_app_get_too_large_number_revision(helpers):
        theapp = pytest.swimlane_instance.apps.get(id=pytest.appid)
        with pytest.raises(ValueError) as excinfo:
            theapp.revisions.get(99)
        assert str(excinfo.value) == pytest.py_ver_no_json()

    @pytest.mark.xfail(reason="SPT-6038: URL is being made with the string, throwing errors")
    def test_app_get_invalid_revision(helpers):
        theapp = pytest.swimlane_instance.apps.get(id=pytest.appid)
        with pytest.raises(ValueError) as excinfo:
            theapp.revisions.get('garbage')
        assert str(excinfo.value) == pytest.py_ver_no_json()

    # This grabs the newest version... not 2 or 3... or errors?
    @pytest.mark.xfail(reason="SPT-6038:Grabbs latest versioninstead of throwing an error")
    def test_app_get_float_revision(helpers):
        theapp = pytest.swimlane_instance.apps.get(id=pytest.appid)
        with pytest.raises(ValueError) as excinfo:
            theapp.revisions.get(2.5)
        assert str(excinfo.value) == 'No JSON object could be decoded'

    @pytest.mark.xfail(reason="SPT-6038?: Attribute error 'list' object has no attribute 'get'")
    def test_app_get_empty_revision(helpers):
        theapp = pytest.swimlane_instance.apps.get(id=pytest.appid)
        with pytest.raises(ValueError) as excinfo:
            theapp.revisions.get('')
        assert str(excinfo.value) == pytest.py_ver_no_json()

    @pytest.mark.xfail(reason="SPT-6038: URL is being made with the None, throwing errors")
    def test_app_get_none_revision(helpers):
        theapp = pytest.swimlane_instance.apps.get(id=pytest.appid)
        with pytest.raises(ValueError) as excinfo:
            theapp.revisions.get(None)
        assert str(excinfo.value) == pytest.py_ver_no_json()
