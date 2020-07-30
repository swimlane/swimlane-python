import pytest
import pendulum


@pytest.fixture(autouse=True, scope='module')
def my_fixture(helpers):
    # setup stuff
    defaultApp = 'one of each type'
    pytest.swimlane_instance = helpers.swimlane_instance
    pytest.app, pytest.appid = helpers.findCreateApp(defaultApp)
    pytest.helpers = helpers
    pytest.newUser1 = pytest.swimlane_instance.users.get(
        display_name=pytest.helpers.createUser()["displayName"])
    pytest.newUser2 = pytest.swimlane_instance.users.get(
        display_name=pytest.helpers.createUser()["displayName"])
    pytest.newUser3 = pytest.swimlane_instance.users.get(
        display_name=pytest.helpers.createUser()["displayName"])
    pytest.delta1 = pendulum.datetime(
        2012, 1, 1, 1, 2, 3) - pendulum.datetime(2011, 12, 31, 22, 2, 3)
    pytest.delta2 = pendulum.datetime(
        2013, 1, 1, 1, 2, 3) - pendulum.datetime(2011, 12, 31, 22, 2, 3)
    pytest.delta3 = pendulum.datetime(
        2012, 10, 1, 1, 2, 3) - pendulum.datetime(2011, 12, 31, 22, 2, 3)
    pytest.app.records.bulk_create({"Text": 'Hello', "Numeric": 123, 'Selection': 'one', 'Date & Time': pendulum.parse("Apr 1, 2020 12:00 AM -06:00"), 'User/Groups': pytest.newUser1, "Timespan": pytest.delta1, "Numeric List": [10, 20, 30], "Text List": ['a', 'b', 'c'], "Multi-select": ['Jan', 'Feb'], "Multi-Select User/Groups": [pytest.newUser1, pytest.newUser2]},
                                   {"Text": 'Hello', "Numeric": -1, 'Selection': 'two', 'Date & Time': pendulum.parse("May 1, 2020 12:00 AM -06:00"), 'User/Groups': pytest.newUser2, "Timespan": pytest.delta2, "Numeric List": [
                                       10, 20, 30], "Text List": ['x', 'y', 'z'], "Multi-select": ['March', 'April'], "Multi-Select User/Groups": [pytest.newUser3, pytest.newUser2]},
                                   {"Text": 'Bye', "Numeric": 123, 'Selection': 'four', 'Date & Time': pendulum.parse("Apr 10, 2020 12:00 AM -06:00"), 'User/Groups': pytest.newUser1, "Timespan": pytest.delta2, "Numeric List": [
                                       20, 40, 60], "Text List": ['a', 'b', 'c'], "Multi-select": ['Jan', 'Feb', 'March'], "Multi-Select User/Groups": [pytest.newUser1, pytest.newUser2]},
                                   {"Text": 'Bye', "Numeric": -1, 'Selection': 'two', 'Date & Time': pendulum.parse("May 1, 2020 12:00 AM -06:00"), 'User/Groups': pytest.newUser3, "Timespan": pytest.delta3, "Numeric List": [
                                       10, 20, 30, 90], "Text List": ['a', 'b', 'c', 'd'], "Multi-select": ['Feb', 'March', 'April'], "Multi-Select User/Groups": [pytest.newUser1, pytest.newUser3]},
                                   {"Text": '123', "Numeric": 0, 'Selection': 'one', 'Date & Time': pendulum.parse("Apr 1, 2020 12:00 AM -06:00"), 'User/Groups': pytest.newUser2, "Timespan": pytest.delta1, "Numeric List": [20, 40, 60], "Text List": ['x', 'y', 'z'], "Multi-select": ['Jan', 'Feb'], "Multi-Select User/Groups": [pytest.newUser1, pytest.newUser3]})
    yield
    # teardown stuff
    helpers.cleanupData()


# equals, doesNotEqual, contains, excludes, lessThan, greaterThan, lessThanOrEqual, greaterThanOrEqual'

class TestAppReportsTextFiltering():
    def test_text_equals(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text', 'equals', 'Hello')
        assert len(report) == 2
        for record in report:
            assert record['Text'] == 'Hello'

    def test_text_does_not_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text', 'doesNotEqual', 'Hello')
        assert len(report) == 3
        for record in report:
            assert record['Text'] != 'Hello'

    def test_text_contains(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text', 'contains', 'e')
        assert len(report) == 4
        for record in report:
            assert 'e' in record['Text']

    def test_text_excludes(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text', 'excludes', 'o')
        assert len(report) == 3
        for record in report:
            assert not '0' in record['Text']

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, this type of filter is not available in the ui")
    def test_text_less_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text', 'lessThan', 'Bye')
        assert len(report) == 1
        for record in report:
            assert record['Text'] < "Bye"

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, this type of filter is not available in the ui")
    def test_text_greater_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text', 'greaterThan', 'Bye')
        assert len(report) == 2
        for record in report:
            assert record['Text'] > "Bye"

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, this type of filter is not available in the ui")
    def test_text_less_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text', 'lessThanOrEqual', 'Bye')
        assert len(report) == 3
        for record in report:
            assert record['Text'] <= "Bye"

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, this type of filter is not available in the ui")
    def test_text_greater_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text', 'greaterThanOrEqual', 'Bye')
        assert len(report) == 4
        for record in report:
            assert record['Text'] >= "Bye"


class TestAppReportsTextListFiltering():
    def test_text_list_equals(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text List', 'equals', ['a', 'b', 'c'])
        assert len(report) == 2
        for record in report:
            assert list(record['Text List']) == ['a', 'b', 'c']

    def test_text_list_does_not_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text List', 'doesNotEqual', ['a', 'b', 'c'])
        assert len(report) == 3
        for record in report:
            assert list(record['Text List']) != ['a', 'b', 'c']

    def test_text_list_contains(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text List', 'contains', ['a', 'b'])
        assert len(report) == 3
        for record in report:
            assert (set(record['Text List']) &
                    set(['a', 'b'])) == set(['a', 'b'])

    def test_text_list_excludes(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text List', 'excludes', ['a', 'b'])
        assert len(report) == 2
        for record in report:
            assert list(set(record['Text List']) & set(['a', 'b'])) == []

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, this type of filter is not available in the ui")
    def test_text_list_less_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text List', 'lessThan', ['e', 'f', 'g'])
        assert len(report) == 1
        for record in report:
            assert record['Text List'] < "Bye"

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, this type of filter is not available in the ui")
    def test_text_list_greater_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text List', 'greaterThan', ['e', 'f', 'g'])
        assert len(report) == 2
        for record in report:
            assert record['Text List'] > "Bye"

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, this type of filter is not available in the ui")
    def test_text_list_less_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text List', 'lessThanOrEqual', ['e', 'f', 'g'])
        assert len(report) == 3
        for record in report:
            assert record['Text List'] <= "Bye"

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, this type of filter is not available in the ui")
    def test_text_list_greater_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Text List', 'greaterThanOrEqual', ['e', 'f', 'g'])
        assert len(report) == 4
        for record in report:
            assert record['Text List'] >= "Bye"


class TestAppReportsNumericFiltering():
    def test_numeric_equals(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Numeric', 'equals', 123)
        assert len(report) == 2
        for record in report:
            assert record['Numeric'] == 123

    def test_numeric_does_not_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Numeric', 'doesNotEqual', 123)
        assert len(report) == 3
        for record in report:
            assert record['Numeric'] != 123

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, contains should only work on list numeric fields")
    def test_numeric_contains(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Numeric', 'contains', 1)
        assert len(report) == 4

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, excludes should only work on list numeric fields")
    def test_numeric_excludes(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Numeric', 'excludes', 1)
        assert len(report) == 3

    def test_numeric_less_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Numeric', 'lessThan', 0)
        assert len(report) == 2
        for record in report:
            assert record['Numeric'] < 0

    def test_numeric_greater_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Numeric', 'greaterThan', 0)
        assert len(report) == 2
        for record in report:
            assert record['Numeric'] > 0

    def test_numeric_less_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Numeric', 'lessThanOrEqual', 0)
        assert len(report) == 3
        for record in report:
            assert record['Numeric'] <= 0

    def test_numeric_greater_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Numeric', 'greaterThanOrEqual', 0)
        assert len(report) == 3
        for record in report:
            assert record['Numeric'] >= 0


class TestAppReportsNumericListFiltering():
    def test_numeric_list_equals(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Numeric List', 'equals', [10, 20, 30])
        assert len(report) == 2
        for record in report:
            assert list(record['Numeric List']) == [10, 20, 30]

    def test_numeric_list_does_not_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Numeric List', 'doesNotEqual', [10, 20, 30])
        assert len(report) == 3
        for record in report:
            assert list(record['Numeric List']) != [10, 20, 30]

    def test_numeric_list_contains(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Numeric List', 'contains', [10, 20])
        assert len(report) == 3

    def test_numeric_list_excludes(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Numeric List', 'excludes', [10, 20])
        assert len(report) == 2

    @pytest.mark.xfail(reason="SPT-6389: This test should have a pyDriver Failure")
    def test_numeric_list_less_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Numeric List', 'lessThan', [10, 20, 30])
        assert len(report) == 2
        for record in report:
            assert record['Numeric List'] < [10, 20, 30]

    @pytest.mark.xfail(reason="SPT-6389: This test should have a pyDriver Failure")
    def test_numeric_list_greater_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Numeric List', 'greaterThan', [10, 20, 30])
        assert len(report) == 2
        for record in report:
            assert record['Numeric List'] > [10, 20, 30]

    @pytest.mark.xfail(reason="SPT-6389: This test should have a pyDriver Failure")
    def test_numeric_list_less_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Numeric List', 'lessThanOrEqual', [10, 20, 30])
        assert len(report) == 3
        for record in report:
            assert record['Numeric List'] <= [10, 20, 30]

    @pytest.mark.xfail(reason="SPT-6389: This test should have a pyDriver Failure")
    def test_numeric_list_greater_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Numeric List', 'greaterThanOrEqual', [10, 20, 30])
        assert len(report) == 3
        for record in report:
            assert record['Numeric List'] >= [10, 20, 30]


class TestAppReportsSelectionFiltering():
    def test_selection_equals(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Selection', 'equals', 'two')
        assert len(report) == 2
        for record in report:
            assert record['Selection'] == 'two'

    def test_selection_does_not_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Selection', 'doesNotEqual', 'two')
        assert len(report) == 3
        for record in report:
            assert record['Selection'] != 'two'

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, contains shouldonly work on mlti-select fields")
    def test_selection_contains(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Selection', 'contains', 'one')
        assert len(report) == 2
        for record in report:
            assert 'one' in record['Selection']

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, excludes shouldonly work on mlti-select fields")
    def test_selection_excludes(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Selection', 'excludes', 'one')
        assert len(report) == 3
        for record in report:
            assert not 'one' in record['Selection']

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, selection should not have gt, lt comparisons")
    def test_selection_less_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Selection', 'lessThan', 'two')
        assert len(report) == 1
        for record in report:
            assert record['Selection'] in ['three', 'four']

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, selection should not have gt, lt comparisons")
    def test_selection_greater_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Selection', 'greaterThan', 'two')
        assert len(report) == 2
        for record in report:
            assert record['Selection'] in ['one']

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, selection should not have gt, lt comparisons")
    def test_selection_less_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Selection', 'lessThanOrEqual', 'two')
        assert len(report) == 3
        for record in report:
            assert record['Selection'] in ['two', 'three', 'four']

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, selection should not have gt, lt comparisons")
    def test_selection_greater_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Selection', 'greaterThanOrEqual', 'two')
        assert len(report) == 4
        for record in report:
            assert record['Selection'] in ['one', 'two']


class TestAppReportsMultiSelectFiltering():
    def test_multi_selection_equals(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Multi-select', 'equals', ['Jan', 'Feb'])
        assert len(report) == 2
        for record in report:
            assert list(record['Multi-select']) == ['Feb', 'Jan']

    def test_multi_selection_does_not_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Multi-select', 'doesNotEqual', ['Jan', 'Feb'])
        assert len(report) == 3
        for record in report:
            assert list(record['Multi-select']) != ['Feb', 'Jan']

    def test_multi_selection_contains(helpers):
        filterList = ['Feb', 'March']
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Multi-select', 'contains', filterList)
        assert len(report) == 2
        for record in report:
            assert all(i in record['Multi-select'] for i in filterList)

    def test_multi_selection_excludes(helpers):
        filterList = ['Feb', 'March']
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Multi-select', 'excludes', filterList)
        assert len(report) == 3
        for record in report:
            assert not all(i in record['Multi-select'] for i in filterList)

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, selection should not have gt, lt comparisons")
    def test_multi_selection_less_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Multi-select', 'lessThan', ['Feb'])
        assert len(report) == 1
        for record in report:
            assert record['Multi-select'] in ['three', 'four']

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, selection should not have gt, lt comparisons")
    def test_multi_selection_greater_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Multi-select', 'greaterThan',  ['Feb'])
        assert len(report) == 2
        for record in report:
            assert record['Multi-select'] in ['one']

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, selection should not have gt, lt comparisons")
    def test_multi_selection_less_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Multi-select', 'lessThanOrEqual',  ['Feb'])
        assert len(report) == 3
        for record in report:
            assert record['Multi-select'] in ['two', 'three', 'four']

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, selection should not have gt, lt comparisons")
    def test_multi_selection_greater_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Multi-select', 'greaterThanOrEqual',  ['Feb'])
        assert len(report) == 4
        for record in report:
            assert record['Multi-select'] in ['one', 'two']


class TestAppReportsDateTimeFiltering():
    def test_date_time_equals(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Date & Time', 'equals', pendulum.parse(
            "May 1, 2020 12:00 AM -06:00"))
        assert len(report) == 2
        for record in report:
            assert record['Date & Time'] == pendulum.parse(
                "May 1, 2020 12:00 AM -06:00")

    def test_date_time_does_not_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Date & Time', 'doesNotEqual',
                      pendulum.parse("May 1, 2020 12:00 AM -06:00"))
        assert len(report) == 3
        for record in report:
            assert record['Date & Time'] != pendulum.parse(
                "May 1, 2020 12:00 AM -06:00")

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, contains should only work on multi-select fields")
    def test_date_time_contains(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Date & Time', 'contains',
                      pendulum.parse("May 1, 2020 12:00 AM -06:00"))
        assert len(report) == 2

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, excludes should only work on multi-select fields")
    def test_date_time_excludes(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Date & Time', 'excludes',
                      pendulum.parse("May 1, 2020 12:00 AM -06:00"))
        assert len(report) == 3

    def test_date_time_less_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Date & Time', 'lessThan', pendulum.parse(
            "Apr 10, 2020 12:00 AM -06:00"))
        assert len(report) == 2
        for record in report:
            assert record['Date & Time'] < pendulum.parse(
                "Apr 10, 2020 12:00 AM -06:00")

    def test_date_time_greater_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Date & Time', 'greaterThan',
                      pendulum.parse("Apr 10, 2020 12:00 AM -06:00"))
        assert len(report) == 2
        for record in report:
            assert record['Date & Time'] > pendulum.parse(
                "Apr 10, 2020 12:00 AM -06:00")

    def test_date_time_less_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Date & Time', 'lessThanOrEqual',
                      pendulum.parse("Apr 10, 2020 12:00 AM -06:00"))
        assert len(report) == 3
        for record in report:
            assert record['Date & Time'] <= pendulum.parse(
                "Apr 10, 2020 12:00 AM -06:00")

    def test_date_time_greater_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Date & Time', 'greaterThanOrEqual',
                      pendulum.parse("Apr 10, 2020 12:00 AM -06:00"))
        assert len(report) == 3
        for record in report:
            assert record['Date & Time'] >= pendulum.parse(
                "Apr 10, 2020 12:00 AM -06:00")


class TestAppReportsTimespanFiltering():
    def test_timespan_equals(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Timespan', 'equals', pytest.delta1)
        assert len(report) == 2
        for record in report:
            assert record['Timespan'] == pytest.delta1

    def test_timespan_does_not_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Timespan', 'doesNotEqual', pytest.delta1)
        assert len(report) == 3
        for record in report:
            assert record['Timespan'] != pytest.delta1

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, contains should not work on timespan fields")
    def test_timespan_contains(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Timespan', 'contains', pytest.delta2)
        assert len(report) == 2

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, contains should not work on timespan fields")
    def test_timespan_excludes(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Timespan', 'excludes',  pytest.delta2)
        assert len(report) == 3

    def test_timespan_less_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Timespan', 'lessThan', pytest.delta3)
        assert len(report) == 2
        for record in report:
            assert record['Timespan'] < pytest.delta3

    def test_timespan_greater_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Timespan', 'greaterThan', pytest.delta3)
        assert len(report) == 2
        for record in report:
            assert record['Timespan'] > pytest.delta3

    def test_timespan_less_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Timespan', 'lessThanOrEqual', pytest.delta3)
        assert len(report) == 3
        for record in report:
            assert record['Timespan'] <= pytest.delta3

    def test_timespan_greater_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Timespan', 'greaterThanOrEqual', pytest.delta3)
        assert len(report) == 3
        for record in report:
            assert record['Timespan'] >= pytest.delta3


class TestAppReportsUserGroupFiltering():
    def test_user_group_equals(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('User/Groups', 'equals', pytest.newUser1)
        assert len(report) == 2
        for record in report:
            assert record['User/Groups'].name == pytest.newUser1.display_name
            assert record['User/Groups'].id == pytest.newUser1.id

    def test_user_group_does_not_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('User/Groups', 'doesNotEqual', pytest.newUser1)
        assert len(report) == 3
        for record in report:
            assert record['User/Groups'].name != pytest.newUser1.display_name
            assert record['User/Groups'].id != pytest.newUser1.id

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, should only work if is multi-select")
    def test_user_group_contains(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('User/Groups', 'contains', pytest.newUser1)
        assert len(report) == 2
        for record in report:
            assert record['User/Groups'].name == pytest.newUser1.display_name
            assert record['User/Groups'].id == pytest.newUser1.id

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, should only work if is multi-select")
    def test_user_group_excludes(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('User/Groups', 'excludes',  pytest.newUser1)
        assert len(report) == 3
        for record in report:
            assert record['User/Groups'].name != pytest.newUser1.display_name
            assert record['User/Groups'].id != pytest.newUser1.id

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, the pyDriver should be throwing an error")
    def test_user_group_less_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('User/Groups', 'lessThan', pytest.newUser1)
        assert len(report) == 2

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, the pyDriver should be throwing an error")
    def test_user_group_greater_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('User/Groups', 'greaterThan', pytest.newUser1)
        assert len(report) == 2

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, the pyDriver should be throwing an error")
    def test_user_group_less_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('User/Groups', 'lessThanOrEqual', pytest.newUser1)
        assert len(report) == 3

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, the pyDriver should be throwing an error")
    def test_user_group_greater_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('User/Groups', 'greaterThanOrEqual', pytest.newUser1)
        assert len(report) == 3


class TestAppReportsMultiSelectUserGroupFiltering():
    def test_multi_select_user_group_equals(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Multi-Select User/Groups', 'equals',
                      [pytest.newUser1, pytest.newUser2])
        assert len(report) == 2
        for record in report:
            userIds = []
            for user in record['Multi-Select User/Groups']:
                userIds.append(user.id)
            assert all(i.id in userIds for i in [
                       pytest.newUser1, pytest.newUser2])

    def test_multi_select_user_group_does_not_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Multi-Select User/Groups', 'doesNotEqual',
                      [pytest.newUser1, pytest.newUser2])
        assert len(report) == 3
        for record in report:
            userIds = []
            for user in record['Multi-Select User/Groups']:
                userIds.append(user.id)
            assert not all(i.id in userIds for i in [
                pytest.newUser1, pytest.newUser2])

    def test_multi_select_user_group_contains(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Multi-Select User/Groups',
                      'contains', [pytest.newUser2])
        assert len(report) == 3
        for record in report:
            assert any(
                user.id == pytest.newUser2.id for user in record['Multi-Select User/Groups'])

    def test_multi_select_user_group_excludes(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Multi-Select User/Groups',
                      'excludes',  [pytest.newUser2])
        assert len(report) == 2
        for record in report:
            assert not any(
                user.id == pytest.newUser2.id for user in record['Multi-Select User/Groups'])

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, the pyDriver should be throwing an error")
    def test_multi_select_user_group_less_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Multi-Select User/Groups', 'lessThan',
                      [pytest.newUser1, pytest.newUser2])
        assert len(report) == 2

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, the pyDriver should be throwing an error")
    def test_multi_select_user_group_greater_than(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Multi-Select User/Groups', 'greaterThan',
                      [pytest.newUser1, pytest.newUser2])
        assert len(report) == 2

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, the pyDriver should be throwing an error")
    def test_multi_select_user_group_less_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Multi-Select User/Groups', 'lessThanOrEqual',
                      [pytest.newUser1, pytest.newUser2])
        assert len(report) == 3

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, the pyDriver should be throwing an error")
    def test_multi_select_user_group_greater_than_or_equal(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Multi-Select User/Groups',
                      'greaterThanOrEqual', [pytest.newUser1, pytest.newUser2])
        assert len(report) == 3


class TestAppReportsOddFieldsFiltering():
    @pytest.mark.xfail(reason="SPT-6389: This actually processes, the pyDriver should be throwing an error")
    def test_attachment_contains(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Attachment', 'contains', None)
        assert len(report) == 2
        for record in report:
            assert record['Attachment'] == pendulum.parse(
                "May 1, 2020 12:00 AM -06:00")

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, the pyDriver should be throwing an error")
    def test_comments_contains(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Comments', 'contains', None)
        assert len(report) == 2
        for record in report:
            assert record['Comments'] == pendulum.parse(
                "May 1, 2020 12:00 AM -06:00")

    @pytest.mark.xfail(reason="SPT-6389: This actually processes, the pyDriver should be throwing an error")
    def test_references_contains(helpers):
        report = pytest.app.reports.build(
            'report-%s' % pytest.fake.word(), limit=0)
        report.filter('Reference', 'contains', None)
        assert len(report) == 2
        for record in report:
            assert record['Reference'] == pendulum.parse(
                "May 1, 2020 12:00 AM -06:00")
