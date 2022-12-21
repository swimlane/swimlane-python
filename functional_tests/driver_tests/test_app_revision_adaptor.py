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

    def test_app_get_specific_revision_float_only_zeros_after_decimal(helpers):
        theapp = pytest.swimlane_instance.apps.get(id=pytest.appid)
        app_rev = theapp.revisions.get(2.0)
        assert app_rev.revision_number == 2.0
        assert app_rev.version.description == pytest.app2.description

    def test_app_get_negative_number_revision(helpers):
        theapp = pytest.swimlane_instance.apps.get(id=pytest.appid)
        with pytest.raises(ValueError) as excinfo:
            theapp.revisions.get(-2)
        assert str(excinfo.value) == 'The revision number must be a positive whole number greater than 0'

    def test_app_get_too_large_number_revision(helpers):
        theapp = pytest.swimlane_instance.apps.get(id=pytest.appid)
        with pytest.raises(ValueError) as excinfo:
            theapp.revisions.get(99)
        assert str(excinfo.value) == pytest.py_ver_no_json()

    def test_app_get_invalid_string_revision(helpers):
        theapp = pytest.swimlane_instance.apps.get(id=pytest.appid)
        with pytest.raises(ValueError) as excinfo:
            theapp.revisions.get('garbage')
        assert str(excinfo.value) == 'The revision number must be a positive whole number greater than 0'

    def test_app_get_float_revision(helpers):
        theapp = pytest.swimlane_instance.apps.get(id=pytest.appid)
        with pytest.raises(ValueError) as excinfo:
            theapp.revisions.get(2.5)
        assert str(excinfo.value) == 'The revision number must be a positive whole number greater than 0'

    def test_app_get_empty_revision(helpers):
        theapp = pytest.swimlane_instance.apps.get(id=pytest.appid)
        with pytest.raises(ValueError) as excinfo:
            theapp.revisions.get('')
        assert str(excinfo.value) == 'The revision number must be a positive whole number greater than 0'

    def test_app_get_none_revision(helpers):
        theapp = pytest.swimlane_instance.apps.get(id=pytest.appid)
        with pytest.raises(ValueError) as excinfo:
            theapp.revisions.get(None)
        assert str(excinfo.value) == 'The revision number must be a positive whole number greater than 0'

    def test_app_get_zero_revision(helpers):
        theapp = pytest.swimlane_instance.apps.get(id=pytest.appid)
        with pytest.raises(ValueError) as excinfo:
            theapp.revisions.get(0)
        assert str(excinfo.value) == 'The revision number must be a positive whole number greater than 0'
