import pytest
from requests import HTTPError


@pytest.fixture(autouse=True, scope='module')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'basic app'
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    pytest.baseRecord = pytest.app.records.create(**{})
    pytest.baseRecord.save()
    pytest.record1 = pytest.baseRecord.for_json()
    pytest.baseRecord["Text"] = pytest.fake.sentence()
    pytest.baseRecord.save()
    pytest.record2 = pytest.baseRecord.for_json()
    pytest.baseRecord["Text"] = pytest.fake.sentence()
    pytest.baseRecord.save()
    pytest.record3 = pytest.baseRecord.for_json()
    pytest.baseRecord["Text"] = pytest.fake.sentence()
    pytest.baseRecord.save()
    pytest.record4 = pytest.baseRecord.for_json()
    yield
    # teardown stuff
    helpers.cleanupData()


class TestRecordRevisionAdaptor:
    def test_record_get_all(helpers):
        therecord = pytest.app.records.get(id=pytest.baseRecord.id)
        revisionList = therecord.revisions.get_all()
        assert len(revisionList) == 4

    def test_record_get_specific_revision(helpers):
        therecord = pytest.app.records.get(id=pytest.baseRecord.id)
        record_rev = therecord.revisions.get(2)
        assert record_rev.revision_number == 2
    def test_record_get_specific_revision_float_only_zeros_after_decimal(helpers):
        therecord = pytest.app.records.get(id=pytest.baseRecord.id)
        record_rev = therecord.revisions.get(2.0)
        assert record_rev.revision_number == 2.0

    def test_record_get_negative_number_revision(helpers):
        therecord = pytest.app.records.get(id=pytest.baseRecord.id)
        with pytest.raises(ValueError) as excinfo:
            therecord.revisions.get(-2)
        assert str(excinfo.value) == 'The revision number must be a positive whole number greater than 0'

    def test_record_get_too_large_number_revision(helpers):
        therecord = pytest.app.records.get(id=pytest.baseRecord.id)
        with pytest.raises(HTTPError) as excinfo:
            therecord.revisions.get(99)
        assert '404 Client Error: Not Found for url' in str(excinfo.value)

    def test_record_get_string_revision(helpers):
        therecord = pytest.app.records.get(id=pytest.baseRecord.id)
        with pytest.raises(ValueError) as excinfo:
            therecord.revisions.get('garbage')
        assert str(excinfo.value) == 'The revision number must be a positive whole number greater than 0'

    def test_record_get_float_revision(helpers):
        therecord = pytest.app.records.get(id=pytest.baseRecord.id)
        with pytest.raises(ValueError) as excinfo:
            therecord.revisions.get(2.5)
        assert str(excinfo.value) == 'The revision number must be a positive whole number greater than 0'

    def test_record_get_empty_revision(helpers):
        therecord = pytest.app.records.get(id=pytest.baseRecord.id)
        with pytest.raises(ValueError) as excinfo:
            therecord.revisions.get('')
        assert str(excinfo.value) == 'The revision number must be a positive whole number greater than 0'

    def test_record_get_none_revision(helpers):
        therecord = pytest.app.records.get(id=pytest.baseRecord.id)
        with pytest.raises(ValueError) as excinfo:
            therecord.revisions.get(None)
        assert str(excinfo.value) == 'The revision number must be a positive whole number greater than 0'

    def test_record_get_zero_revision(helpers):
        therecord = pytest.app.records.get(id=pytest.baseRecord.id)
        with pytest.raises(ValueError) as excinfo:
            therecord.revisions.get(0)
        assert str(excinfo.value) == 'The revision number must be a positive whole number greater than 0'