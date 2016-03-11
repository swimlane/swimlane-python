import unittest
import uuid

from swimlane.core.resources import App, Record, Report, StatsReport
from swimlane.core.search import Search, filtering, groupby, aggregate

class SearchTestCase(unittest.TestCase):
    pass

"""
APP_ID = "567490ad55d95d5c30d02266"
USER_ID = "5674909d55d95d5c30d02200"
REPORT_ID = "5686d8f755d95d19bcd60664"


def test_create(default_client):
    report = Report.find(REPORT_ID)
    assert Search(report)


def test_execute_report(default_client):
    app = App.find(app_id=APP_ID)

    one_id = app.fields[0]["id"]
    one_value = str(uuid.uuid1())

    two_id = app.fields[1]["id"]
    two_value = str(uuid.uuid1())

    record = Record.new_for(APP_ID)
    record.values[one_id] = one_value
    record.values[two_id] = two_value
    record.insert()

    report = Report.new_for(APP_ID, USER_ID, "Test")
    report.columns = [one_id, two_id]
    report.filters.append(filtering.create_filter(one_id, filtering.EQ, one_value))

    result = Search(report).execute()

    assert result
    assert result.count == 1
    assert result.offset == 0
    assert result.limit == report.pageSize

    records = list(result.records)

    assert records
    assert len(records) == 1
    assert records[0].values[one_id] == one_value
    assert records[0].values[two_id] == two_value

    report = Report.new_for(APP_ID, USER_ID, "Test")
    report.columns = [one_id, two_id]
    report.keywords = one_value

    result = Search(report).execute()

    assert result
    assert result.count > 0


def test_execute_statsreport(default_client):
    app = App.find(app_id=APP_ID)

    one_id = app.fields[0]["id"]

    report = StatsReport.new_for(APP_ID, USER_ID, "Test")
    report.groupBys = [groupby.create_groupby(one_id, groupby.HOUR)]
    stats = list(Search(report).execute().stats)

    assert stats
    assert len(stats) > 0
    assert stats[0].groups[one_id] == u"No Value"


def test_execute_report_paging(default_client):
    app = App.find(app_id=APP_ID)

    one_id = app.fields[0]["id"]
    one_value = str(uuid.uuid1())

    two_id = app.fields[1]["id"]
    two_value = str(uuid.uuid1())

    report = Report.new_for(APP_ID, USER_ID, "Test")
    report.columns = [one_id, two_id]
    report.pageSize = 7
    report.filters.append(filtering.create_filter(one_id, filtering.CONTAINS, "a"))

    search = Search(report)
    result = search.execute()
    total = result.count
    count = len(list(result.records))
    while search.has_more_pages:
        result = search.next_page()
        count += len(list(result.records))

    assert total == count
"""
