import pytest


@pytest.fixture(autouse=True, scope='module')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'basic app'
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    pytest.py_ver = helpers.py_ver
    pytest.py_ver_no_json = helpers.py_ver_no_json
    pytest.py_ver_missing_param = helpers.py_ver_missing_param
    pytest.app.records.bulk_create({"Text": 'Hello', "Numeric": 123},
                                   {"Text": 'Hello', "Numeric": -1},
                                   {"Text": 'Bye', "Numeric": 123},
                                   {"Text": 'Bye', "Numeric": -
                                       1, "Selection": "123"},
                                   {"Text": '123', "Numeric": 0})
    yield
    # teardown stuff
    helpers.cleanupData()


class TestAppReportsList():
    def test_list_count(helpers):
        reportList = pytest.app.reports.list()
        assert len(reportList) == 1


class TestReportBuildAdaptor:
    def test_build_report(helpers):
        report = pytest.app.reports.build('report-%s' % pytest.fake.word())
        assert len(report) == 5

    def test_build_report_keywords_string(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), keywords=['Hello'])
        assert len(report) == 2

    def test_build_report_keywords_numeric(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), keywords=["123"])
        assert len(report) == 2

    def test_build_report_no_name(helpers):
        with pytest.raises(TypeError) as excinfo:
            pytest.app.reports.build()
        assert str(excinfo.value) == 'build() {}'.format(
            pytest.py_ver_missing_param(2, 1, "name", "exactly"))

    def test_build_report_no_name_with_limit(helpers):
        with pytest.raises(TypeError) as excinfo:
            pytest.app.reports.build(limit=0)
        assert str(excinfo.value) == 'build() {}'.format(
            pytest.py_ver_missing_param(2, 1, "name", "exactly"))

    def test_build_report_limit_less_then_total(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=2)
        assert len(report) == 2

    def test_build_report_limit_more_then_total(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=10)
        assert len(report) == 5

    def test_build_report_limit_zero(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        assert len(report) == 5

    @pytest.mark.xfail(reason="SPT-6308: The limit value should be a whole number of at least zero")
    def test_build_report_limit_below_zero(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=-5)
        assert len(report) == 1

    @pytest.mark.xfail(reason="SPT-6308: The limit value should be a whole number of at least zero")
    def test_build_report_limit_fraction(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=2.5)
        assert len(report) == 2


class TestReportFilteringAdaptor:
    def test_reporting_one_filter(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text', 'equals', 'Hello')
        assert len(report) == 2
        for record in report:
            assert record['Text'] == 'Hello'

    def test_reporting_two_filter(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text', 'equals', 'Hello')
        report.filter('Numeric', 'equals', -1)
        assert len(report) == 1
        for record in report:
            assert record['Text'] == 'Hello'
            assert record['Numeric'] == -1

    def test_reporting_one_filter_no_match(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text', 'equals', 'garbage')
        assert len(report) == 0

    def test_reporting_two_filter_no_match(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text', 'equals', 'Hello')
        report.filter('Text', 'equals', 'Bye')
        assert len(report) == 0

    def test_reporting_filter_none_value(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text', 'equals', None)
        assert len(report) == 0

    def test_reporting_filter_random_field_name(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        fieldName = pytest.fake.isbn10()
        with pytest.raises(KeyError) as excinfo:
            report.filter(fieldName, 'equals', 'Hello')
        assert str(excinfo.value) == '"<App: %s> has no field \'%s\'"' % (
            pytest.app, fieldName)

    def test_reporting_filter_similar_field_name(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        fieldName = 'texts'
        with pytest.raises(KeyError) as excinfo:
            report.filter(fieldName, 'equals', 'Hello')
        assert str(excinfo.value) == '"<App: %s> has no field \'%s\'. Similar fields: %s\'Text\'"' % (
            pytest.app, fieldName, 'u' if (pytest.py_ver() == 2) else '')

    def test_reporting_filter_case_insensitive_field_name(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        fieldName = 'TEXT'
        with pytest.raises(KeyError) as excinfo:
            report.filter(fieldName, 'equals', 'Hello')
        assert str(excinfo.value) == '"<App: %s> has no field \'%s\'"' % (
            pytest.app, fieldName)

    def test_reporting_filter_random_comparison_name(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        comparison = pytest.fake.word()
        with pytest.raises(ValueError) as excinfo:
            report.filter('Text', comparison, 'Hello')
        assert str(excinfo.value) == 'Operand must be one of equals, doesNotEqual, contains, excludes, lessThan, greaterThan, lessThanOrEqual, greaterThanOrEqual'

    # should we be checking this somewhere?
    def test_reporting_filter_bad_value_type(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        with pytest.raises(ValueError) as excinfo:
            report.filter('Numeric', 'equals', 'Hello')

    def test_reporting_invalid_field_name_type_None(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        fieldName = None
        with pytest.raises(ValueError) as excinfo:
            report.filter(fieldName, 'equals', 'Hello')
        assert str(excinfo.value) == "field_name is of an invalid format, expected non-empty string"

    def test_reporting_invalid_field_name_type_number(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        fieldName = 1234
        with pytest.raises(ValueError) as excinfo:
            report.filter(fieldName, 'equals', 'Hello')
        assert str(excinfo.value) == "field_name is of an invalid format, expected non-empty string"

    def test_reporting_invalid_field_name_type_object(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        fieldName = {"Name": "Text"}
        with pytest.raises(ValueError) as excinfo:
            report.filter(fieldName, 'equals', 'Hello')
        assert str(excinfo.value) == "field_name is of an invalid format, expected non-empty string"
    
    def test_reporting_invalid_field_name_empty(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        fieldName = ''
        with pytest.raises(ValueError) as excinfo:
            report.filter(fieldName, 'equals', 'Hello')
        assert str(excinfo.value) == "field_name is of an invalid format, expected non-empty string"

    def test_reporting_missing_params(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        with pytest.raises(TypeError) as excinfo:
            report.filter('Text',  'equals')
        assert str(excinfo.value) == 'filter() {}'.format(
            pytest.py_ver_missing_param(4, 3, "value", "exactly"))


class TestAppReportsGet():
    def test_get_report_id(helpers):
        reportList = pytest.app.reports.list()
        areport = pytest.app.reports.get(reportList[0]._raw['id'])
        assert reportList[0]._raw == areport._raw

    def test_get_report_no_id(helpers):
        with pytest.raises(TypeError) as excinfo:
            pytest.app.reports.get()
        assert str(excinfo.value) == 'get() {}'.format(
            pytest.py_ver_missing_param(2, 1, "report_id", "exactly"))

    # Looks like we are not verifying the valid type for the id?
    @pytest.mark.xfail(reason="SPT-6297: Pydriver should verify that the reportID should be a valid value")
    def test_get_report_null_id(helpers):
        reportID = None
        with pytest.raises(TypeError) as excinfo:
            pytest.app.reports.get(reportID)
        assert str(excinfo.value) == 'get() takes exactly 2 arguments (1 given)'

    # Looks like we are not verifying the valid type for the id?
    @pytest.mark.xfail(reason="SPT-6297: Pydriver should verify that the reportID should be a valid value")
    def test_get_report_empty_id(helpers):
        reportID = ''
        with pytest.raises(TypeError) as excinfo:
            pytest.app.reports.get(reportID)
        assert str(excinfo.value) == 'get() takes exactly 2 arguments (1 given)'

    # Is this the proper response for a report ID that does not exist?
    def test_get_report_garbage_id(helpers):
        reportID = 'garbage'
        with pytest.raises(ValueError) as excinfo:
            pytest.app.reports.get(reportID)
        assert str(excinfo.value) == pytest.py_ver_no_json()

    # Looks like we are not verifying the valid type for the id?
    @pytest.mark.xfail(reason="SPT-6297: Pydriver should verify that the reportID should be a valid value")
    def test_get_report_with_report_object(helpers):
        reportList = pytest.app.reports.list()
        with pytest.raises(TypeError) as excinfo:
            pytest.app.reports.get(reportList[0])
        assert str(excinfo.value) == pytest.py_ver_no_json()
