import pytest
from swimlane import exceptions


@pytest.fixture(autouse=True, scope='module')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'selection fields'
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.py_ver = helpers.py_ver
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    pytest.single_select_falues = ['four', 'three', 'two', 'one']
    yield
    # teardown stuff
    helpers.cleanupData()


class TestRequiredSelectionField:
    def test_required_field(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a"})
        assert theRecord["Required Single-select"] == "a"

    def test_required_field_not_set(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(**{"Single-select": "two"})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Required field "Required Single-select" is not set' % pytest.app.acronym

    def test_required_field_not_set_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a"})
        theRecord["Required Single-select"] = None
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord.save()
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Required field "Required Single-select" is not set' % theRecord.tracking_id


class TestSingleSelectField:
    def test_single_select_field(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a", "Single-select": "two"})
        assert theRecord["Single-select"] == "two"

    def test_single_select_field_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a"})
        theRecord["Single-select"] = "two"
        theRecord.save()

    def test_single_select_field_multiple(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Single-select": "a", "Single-select": ["two", "three"]})
        assert str(excinfo.value) == "Validation failed for <Record: {} - New>. Reason: Field 'Single-select' expects one of '{}', got 'list' instead".format(
            pytest.app.acronym, ("str", "basestring")[pytest.py_ver() == 2])

    def test_single_select_field_multiple_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a"})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Single-select"] = ["two", "three"]
        assert str(excinfo.value) == "Validation failed for <Record: {}>. Reason: Field 'Single-select' expects one of '{}', got 'list' instead".format(
            theRecord.tracking_id, ("str", "basestring")[pytest.py_ver() == 2])

    def test_single_select_field_empty(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Single-select": "a", "Single-select": ""})
        assert str(excinfo.value) == 'Validation failed for <Record: {} - New>. Reason: Field "Single-select" invalid value "". Valid options: {}'.format(
            pytest.app.acronym, ', '.join(pytest.single_select_falues[::(-1, 1)[pytest.py_ver() == 2]]))

    def test_single_select_field_empty_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a"})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Single-select"] = ""
        assert str(excinfo.value) == 'Validation failed for <Record: {}>. Reason: Field "Single-select" invalid value "". Valid options: {}'.format(
            theRecord.tracking_id, ', '.join(pytest.single_select_falues[::(-1, 1)[pytest.py_ver() == 2]]))

    def test_single_select_field_none(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a", "Single-select": None})
        assert theRecord["Single-select"] == None

    def test_single_select_field_none_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a"})
        theRecord["Single-select"] = None
        theRecord.save()

    def test_single_select_field_case_sensitive(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Single-select": "a", "Single-select": "ONE"})
        assert str(excinfo.value) == 'Validation failed for <Record: {} - New>. Reason: Field "Single-select" invalid value "ONE". Valid options: {}'.format(
            pytest.app.acronym, ', '.join(pytest.single_select_falues[::(-1, 1)[pytest.py_ver() == 2]]))

    def test_single_select_field_case_sensitive_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a"})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Single-select"] = "ONE"
        assert str(excinfo.value) == 'Validation failed for <Record: {}>. Reason: Field "Single-select" invalid value "ONE". Valid options: {}'.format(
            theRecord.tracking_id, ', '.join(pytest.single_select_falues[::(-1, 1)[pytest.py_ver() == 2]]))

    def test_single_select_field_int(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Single-select": "a", "Single-select": 1})
        assert str(excinfo.value) == "Validation failed for <Record: {} - New>. Reason: Field 'Single-select' expects one of '{}', got 'int' instead".format(
            pytest.app.acronym, ("str", "basestring")[pytest.py_ver() == 2])

    def test_single_select_field_int_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a"})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Single-select"] = 123
        assert str(excinfo.value) == "Validation failed for <Record: {}>. Reason: Field 'Single-select' expects one of '{}', got 'int' instead".format(
            theRecord.tracking_id, ("str", "basestring")[pytest.py_ver() == 2])


class TestMultiSelectField:
    def test_multi_select_field(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a", "Multi-select": ["first", "fourth"]})
        assert list(theRecord["Multi-select"]) == ["first", "fourth"]

    def test_multi_select_field_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a"})
        theRecord["Multi-select"] = ["first", "fourth"]
        theRecord.save()

    @pytest.mark.xfail(reason="SPT-6356: Should we turn a string into a list??")
    def test_multi_select_field_single_value(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a", "Multi-select": "first"})
        assert list(theRecord["Multi-select"]) == ["first"]

    @pytest.mark.xfail(reason="SPT-6356: Should we turn a string into a list??")
    def test_multi_select_field_single_value_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a"})
        theRecord["Multi-select"] = "first"
        theRecord.save()

    def test_multi_select_field_deselect_value_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a", "Multi-select": ["first", "fourth"]})
        theRecord["Multi-select"].deselect("fourth")
        theRecord.save()
        assert list(theRecord["Multi-select"]) == ["first"]

    def test_multi_select_field_deselect_unused_value_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a", "Multi-select": ["first", "fourth"]})
        with pytest.raises(KeyError) as excinfo:
            theRecord["Multi-select"].deselect("third")
        assert str(excinfo.value) == "'third'"

    def test_multi_select_field_select_unused_value_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a", "Multi-select": ["first", "second"]})
        theRecord["Multi-select"].select("fourth")
        theRecord.save()
        assert list(theRecord["Multi-select"]) == ["first", "fourth", "second"]

    def test_multi_select_field_select_used_value_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a", "Multi-select": ["first", "second"]})
        theRecord["Multi-select"].select("second")
        theRecord.save()
        assert list(theRecord["Multi-select"]) == ["first", "second"]

    def test_multi_select_field_select_value_int_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a", "Multi-select": ["first", "second"]})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Multi-select"].select(2)
        assert str(excinfo.value) == "Validation failed for <Record: {}>. Reason: Field 'Multi-select' expects one of '{}', got 'int' instead".format(
            theRecord.tracking_id, ("str", "basestring")[pytest.py_ver() == 2])

    def test_multi_select_field_deselect_value_int_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a", "Multi-select": ["first", "second"]})
        with pytest.raises(KeyError) as excinfo:
            theRecord["Multi-select"].deselect(2)
        assert str(excinfo.value) == "2"


class TestReadOnlySelectField:
    def test_read_only_field(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Single-select": "a", "Read-only Single-select": "aa"})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Cannot set readonly field \'Read-only Single-select\'' % pytest.app.acronym

    def test_read_only_field_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a"})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Read-only Single-select"] = "aa"
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Cannot set readonly field \'Read-only Single-select\'' % theRecord.tracking_id


class TestDefaultSelectField:
    def test_default_value_select_field(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a"})
        assert theRecord["Default Value Single-select"] == "y"

    def test_default_value_select_field_set_on_create(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a", "Default Value Single-select": "z"})
        assert theRecord["Default Value Single-select"] == "z"

    def test_default_value_select_field_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a"})
        theRecord["Default Value Single-select"] = "x"
        theRecord.save()
        assert theRecord["Default Value Single-select"] == "x"


class TestDefaultMultiSelectField:
    def test_default_value_multi_select_field(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a"})
        assert list(theRecord["Default Value Multi-select"]
                    ) == ["Adam", "Charlie"]

    def test_default_value_multi_select_field_set_on_create(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a", "Default Value Multi-select": ["Brad"]})
        assert list(theRecord["Default Value Multi-select"]) == ["Brad"]

    def test_default_value_multi_select_field_on_save(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Single-select": "a"})
        theRecord["Default Value Multi-select"] = ["Davis"]
        theRecord.save()
        assert list(theRecord["Default Value Multi-select"]) == ["Davis"]
