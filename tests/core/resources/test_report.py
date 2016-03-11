import unittest

from swimlane.core.resources import App, Record, Report
from swimlane.core.search.filtering import create_filter, EQ

class ReportTestCase(unittest.TestCase):
    pass

"""
APP_ID = "567490ad55d95d5c30d02266"
USER_ID = "5674909d55d95d5c30d02200"
NAME = "A Test Report"
REPORT_ID = "5686d8f755d95d19bcd60664"


def test_new_for():
    report = Report.new_for(APP_ID, USER_ID, NAME)
    assert report.offset == 0
    assert not report.disabled
    assert APP_ID in report.applicationIds
    assert report.createdByUser
    assert report.modifiedByUser
    assert report.createdDate
    assert report.modifiedDate
    assert report.name == NAME


def test_find_all(default_client):
    reports = Report.find_all()
    assert reports
    assert len(list(reports)) > 0
    reports = Report.find_all(app_id=APP_ID)
    assert reports
    assert len(list(reports)) > 0


def test_find(default_client):
    report = Report.find(REPORT_ID)
    assert report
    assert not report.disabled


def test_insert(default_client):
    app = App.find(app_id=APP_ID)
    assert app
    report = Report.new_for(APP_ID, USER_ID, NAME)
    report.filters.append(create_filter(app.fields[0]["id"], EQ, "nothing"))
    report.insert()


def test_update(default_client):
    app = App.find(app_id=APP_ID)
    assert app
    report = Report.find(REPORT_ID)
    assert report
    filter_count = len(report.filters)
    report.filters.append(create_filter(app.fields[0]["id"], EQ, "nothing"))
    report.update()
    report = Report.find(REPORT_ID)
    assert report
    assert len(report.filters) == (filter_count + 1)
"""
