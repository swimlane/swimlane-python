import pytest
from swimlane import exceptions


@pytest.fixture(autouse=True, scope='module')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'numeric fields'
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    pytest.py_ver_string_type = helpers.py_ver_string_type
    yield
    # teardown stuff
    helpers.cleanupData()


class TestRequiredNumericField:
    def test_required_field(helpers):
        theRecord = pytest.app.records.create(**{"Required Numeric": 101})
        assert theRecord["Required Numeric"] == 101

    def test_required_field_not_set(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(**{"Numeric": 2468})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Required field "Required Numeric" is not set' % pytest.app.acronym


class TestUniqueNumericField:
    @pytest.mark.xfail(reason="SPT-6357: API call throws a 500 on the duplicate unique value.")
    def test_unique_field_duplicate(helpers):
        uniqueNumeric = 111
        firstRecord = pytest.app.records.create(
            **{"Required Numeric": 101, "Unique Numeric": uniqueNumeric})
        assert firstRecord["Unique Numeric"] == uniqueNumeric
        # This needs to handle an exception on this call.
        pytest.app.records.create(
            **{"Required Numeric": 101, "Unique Numeric": uniqueNumeric})

    @pytest.mark.xfail(reason="SPT-6357: API call throws a 500 on the duplicate unique value.")
    def test_unique_field_duplicate_on_save(helpers):
        uniqueNumeric = 222
        firstRecord = pytest.app.records.create(
            **{"Required Numeric": 101, "Unique Numeric": uniqueNumeric})
        assert firstRecord["Unique Numeric"] == uniqueNumeric
        secondRecord = pytest.app.records.create(**{"Required Numeric": 101})
        secondRecord["Unique Numeric"] = uniqueNumeric
        secondRecord.save()


class TestCalculatedNumericField:
    def test_calculated_Numeric_field(helpers):
        NumericValue = pytest.fake.random_int()
        theRecord = pytest.app.records.create(
            **{"Required Numeric": 101, "Numeric": NumericValue})
        assert theRecord["Calculated Numeric"] == NumericValue + 1

    def test_calculated_Numeric_field_on_save(helpers):
        NumericValue = pytest.fake.random_int()
        theRecord = pytest.app.records.create(**{"Required Numeric": 101})
        theRecord["Numeric"] = NumericValue
        theRecord.save()
        assert theRecord["Calculated Numeric"] == NumericValue + 1


class TestListNumericField:
    def test_list_Numeric_field(helpers):
        NumericValue = pytest.fake.pylist(
            pytest.fake.random_digit(), True, 'int')
        pytest.app.records.create(
            **{"Required Numeric": 101, "Numeric List": NumericValue})

    def test_list_Numeric_field_on_save(helpers):
        NumericValue = pytest.fake.pylist(
            pytest.fake.random_digit(), True, 'int')
        theRecord = pytest.app.records.create(**{"Required Numeric": 101})
        theRecord['Numeric List'] = NumericValue
        theRecord.save()

    def test_list_Numeric_field_on_save_reverse(helpers):
        NumericValue = pytest.fake.pylist(5, True, 'int')
        theRecord = pytest.app.records.create(
            **{"Required Numeric": 101, "Numeric List": NumericValue})
        theRecord['Numeric List'].reverse()
        theRecord.save()
        assert list(theRecord['Numeric List']) == NumericValue[::-1]

    def test_list_Numeric_field_on_save_insert(helpers):
        NumericValue = pytest.fake.pylist(5, True, 'int')
        newValue = pytest.fake.random_int()
        theRecord = pytest.app.records.create(
            **{"Required Numeric": 101, "Numeric List": NumericValue})
        theRecord['Numeric List'].insert(2, newValue)
        NumericValue.insert(2, newValue)
        theRecord.save()
        assert list(theRecord['Numeric List']) == NumericValue

    def test_list_Numeric_field_on_save_insert_bad_value(helpers):
        NumericValue = pytest.fake.pylist(5, True, 'int')
        newValue = pytest.fake.word()
        theRecord = pytest.app.records.create(
            **{"Required Numeric": 101, "Numeric List": NumericValue})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord['Numeric List'].insert(2, newValue)
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Numeric list field items must be numbers, not "%s"' % (
            theRecord.tracking_id, pytest.py_ver_string_type())

    def test_list_Numeric_field_on_save_append(helpers):
        NumericValue = pytest.fake.pylist(5, True, 'int')
        newValue = pytest.fake.random_int()
        theRecord = pytest.app.records.create(
            **{"Required Numeric": 101, "Numeric List": NumericValue})
        theRecord['Numeric List'].append(newValue)
        NumericValue.append(newValue)
        theRecord.save()
        assert list(theRecord['Numeric List']) == NumericValue

    def test_list_Numeric_field_on_save_append_bad_value(helpers):
        NumericValue = pytest.fake.pylist(5, True, 'int')
        newValue = pytest.fake.word()
        theRecord = pytest.app.records.create(
            **{"Required Numeric": 101, "Numeric List": NumericValue})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord['Numeric List'].append(newValue)
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Numeric list field items must be numbers, not "%s"' % (
            theRecord.tracking_id, pytest.py_ver_string_type())


class TestMinValueNumericField:
    def test_min_count_exact(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Numeric": 101, "Min Numeric": 3})
        assert theRecord["Min Numeric"] == 3

    def test_min_count_on_save_exact(helpers):
        theRecord = pytest.app.records.create(**{"Required Numeric": 101})
        theRecord["Min Numeric"] = 3
        theRecord.save()

    def test_min_count_more(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Numeric": 101, "Min Numeric": 5})
        assert theRecord["Min Numeric"] == 5

    def test_min_count_on_save_more(helpers):
        theRecord = pytest.app.records.create(**{"Required Numeric": 101})
        theRecord["Min Numeric"] = 5
        theRecord.save()

    def test_min_count_too_low(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Numeric": 101, "Min Numeric": 2})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Field "Min Numeric" minimum value "3.0", received "2"' % pytest.app.acronym

    def test_min_count_on_save_too_low(helpers):
        theRecord = pytest.app.records.create(**{"Required Numeric": 101})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Min Numeric"] = 2
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Field "Min Numeric" minimum value "3.0", received "2"' % theRecord.tracking_id


class TestMaxValueNumericField:
    def test_max_value_exact(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Numeric": 101, "Max Numeric": 100})
        assert theRecord["Max Numeric"] == 100

    def test_max_value_on_save_exact(helpers):
        theRecord = pytest.app.records.create(**{"Required Numeric": 101})
        theRecord["Max Numeric"] = 100
        theRecord.save()

    def test_max_value_more(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Numeric": 101, "Max Numeric": 5})
        assert theRecord["Max Numeric"] == 5

    def test_max_value_on_save_more(helpers):
        theRecord = pytest.app.records.create(**{"Required Numeric": 101})
        theRecord["Max Numeric"] = 5
        theRecord.save()

    def test_max_value_too_high(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Numeric": 101, "Max Numeric": 102})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Field "Max Numeric" maximum value "100.0", received "102"' % pytest.app.acronym

    def test_max_value_on_save_too_high(helpers):
        theRecord = pytest.app.records.create(**{"Required Numeric": 101})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Max Numeric"] = 102
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Field "Max Numeric" maximum value "100.0", received "102"' % theRecord.tracking_id


class TestMinMaxValueNumericField:
    def test_min_count_exact(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Numeric": 101, "Min Max Numeric": 3})
        assert theRecord["Min Max Numeric"] == 3

    def test_min_count_on_save_exact(helpers):
        theRecord = pytest.app.records.create(**{"Required Numeric": 101})
        theRecord["Min Max Numeric"] = 3
        theRecord.save()

    def test_max_value_exact(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Numeric": 101, "Min Max Numeric": 100})
        assert theRecord["Min Max Numeric"] == 100

    def test_max_value_on_save_exact(helpers):
        theRecord = pytest.app.records.create(**{"Required Numeric": 101})
        theRecord["Min Max Numeric"] = 100
        theRecord.save()

    def test_min_count_more(helpers):
        theRecord = pytest.app.records.create(
            **{"Required Numeric": 101, "Min Max Numeric": 5})
        assert theRecord["Min Max Numeric"] == 5

    def test_min_count_on_save_more(helpers):
        theRecord = pytest.app.records.create(**{"Required Numeric": 101})
        theRecord["Min Max Numeric"] = 5
        theRecord.save()

    def test_min_count_too_low(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Numeric": 101, "Min Max Numeric": 2})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Field "Min Max Numeric" minimum value "3.0", received "2"' % pytest.app.acronym

    def test_min_count_on_save_too_low(helpers):
        theRecord = pytest.app.records.create(**{"Required Numeric": 101})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Min Max Numeric"] = 2
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Field "Min Max Numeric" minimum value "3.0", received "2"' % theRecord.tracking_id

    def test_max_value_too_high(helpers):
        with pytest.raises(exceptions.ValidationError) as excinfo:
            pytest.app.records.create(
                **{"Required Numeric": 101, "Min Max Numeric": 102})
        assert str(excinfo.value) == 'Validation failed for <Record: %s - New>. Reason: Field "Min Max Numeric" maximum value "100.0", received "102"' % pytest.app.acronym

    def test_max_value_on_save_too_high(helpers):
        theRecord = pytest.app.records.create(**{"Required Numeric": 101})
        with pytest.raises(exceptions.ValidationError) as excinfo:
            theRecord["Min Max Numeric"] = 102
        assert str(excinfo.value) == 'Validation failed for <Record: %s>. Reason: Field "Min Max Numeric" maximum value "100.0", received "102"' % theRecord.tracking_id
