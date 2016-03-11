import unittest

from swimlane.core.resources import App, Record, StatsReport
from swimlane.core.search.filtering import create_filter, EQ

APP_ID = "567490ad55d95d5c30d02266"


class StatsReportTestCase(unittest.TestCase):
    pass

"""
USER_ID = "5674909d55d95d5c30d02200"
NAME = "A Test StatsReport Report"
REPORT_ID = "5686d8f755d95d19bcd60664"


def test_new_for():
    report = StatsReport.new_for(APP_ID, USER_ID, NAME)
    assert report.offset == 0
    assert not report.disabled
    assert APP_ID in report.applicationIds
    assert report.createdByUser
    assert report.modifiedByUser
    assert report.createdDate
    assert report.modifiedDate
    assert report.name == NAME
    assert report.chartOptions
    assert report.chartOptions["showLegend"]

def test_find_all(default_client):
    reports = StatsReport.find_all()
    assert reports
    assert len(list(reports)) > 0
    reports = StatsReport.find_all(app_id=APP_ID)
    assert reports
    assert len(list(reports)) > 0


def test_find(default_client):
    report = StatsReport.find(REPORT_ID)
    assert report
    assert not report.disabled


def test_insert(default_client):
    app = App.find(app_id=APP_ID)
    assert app
    report = StatsReport.new_for(APP_ID, USER_ID, NAME)
    report.filters.append(create_filter(app.fields[0]["id"], EQ, "nothing"))
    report.insert()


def test_update(default_client):
    app = App.find(app_id=APP_ID)
    assert app
    report = StatsReport.find(REPORT_ID)
    assert report
    filter_count = len(report.filters)
    report.filters.append(create_filter(app.fields[0]["id"], EQ, "nothing"))
    report.update()
    report = StatsReport.find(REPORT_ID)
    assert report
    assert len(report.filters) == (filter_count + 1)
"""
