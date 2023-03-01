import pytest
import pendulum


@pytest.fixture(autouse=True, scope='module')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'history field'
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    yield
    # teardown stuff
    helpers.cleanupData()


class TestHistoryField:
    def test_history_field(helpers):
        theRecord = pytest.app.records.create(**{})
        assert len(theRecord["history"]) == 1
        assert theRecord["history"][0].user.name == "admin"

    def test_history_field_multiple_revs(helpers):
        theRecord = pytest.app.records.create(**{"Text": "Create"})
        theRecord["Text"] = "First Edit"
        theRecord.save()
        theRecord["Text"] = "Second Edit"
        theRecord.save()
        theRecord["Text"] = "Third Edit"
        theRecord.save()
        assert len(theRecord["history"]) == 4

    def test_history_field_multiple_changes_one_save(helpers):
        theRecord = pytest.app.records.create(**{"Text": "Create"})
        theRecord["Text"] = "First Edit"
        theRecord["Text"] = "Second Edit"
        theRecord["Text"] = "Third Edit"
        theRecord.save()
        assert len(theRecord["history"]) == 2

    def test_history_field_edit_version(helpers):
        theRecord = pytest.app.records.create(**{"Text": "Create"})
        theRecord["Text"] = "First Edit"
        theRecord.save()
        with pytest.raises(AttributeError) as excinfo:
            theRecord["history"][1].version = "400"
        assert str(excinfo.value) == "can't set attribute"

    def test_history_field_edit_revision_number(helpers):
        theRecord = pytest.app.records.create(**{"Text": "Create"})
        theRecord["Text"] = "First Edit"
        theRecord.save()
        with pytest.raises(AttributeError) as excinfo:
            theRecord["history"][1].revision_number = "400"
        assert str(excinfo.value) == "can't set attribute"

    def test_history_field_edit_modified_date(helpers):
        theRecord = pytest.app.records.create(**{"Text": "Create"})
        theRecord["Text"] = "First Edit"
        theRecord.save()
        with pytest.raises(AttributeError) as excinfo:
            theRecord["history"][1].modified_date = pendulum.now()
        assert str(excinfo.value) == "can't set attribute"

    def test_history_field_edit_app_version(helpers):
        theRecord = pytest.app.records.create(**{"Text": "Create"})
        theRecord["Text"] = "First Edit"
        theRecord.save()
        with pytest.raises(AttributeError) as excinfo:
            theRecord["history"][1].app_version = 123
        assert str(excinfo.value) == "can't set attribute"

    def test_history_field_edit_app_revision_number(helpers):
        theRecord = pytest.app.records.create(**{"Text": "Create"})
        theRecord["Text"] = "First Edit"
        theRecord.save()
        with pytest.raises(AttributeError) as excinfo:
            theRecord["history"][1].app_revision_number = 123
        assert str(excinfo.value) == "can't set attribute"

    def test_history_field_edit_user(helpers):
        theRecord = pytest.app.records.create(**{"Text": "Create"})
        swimUser = pytest.swimlane_instance.users.get(display_name="admin")
        theRecord["Text"] = "First Edit"
        theRecord.save()
        with pytest.raises(AttributeError) as excinfo:
            theRecord["history"][1].user = swimUser
        assert str(excinfo.value) == "can't set attribute"
