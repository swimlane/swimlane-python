"""This module provides a StatsReport class."""

from .. import SwimlaneDict
from .report import Report

TEMPLATE = list({
    "$type": "Core.Models.Search.StatsReport, Core",
    "chartOptions": {
        "showLegend": True,
        "showLabels": True,
        "showXAxis": True,
        "showYAxis": True,
        "showXAxisLabel": False,
        "showYAxisLabel": False,
        "xAxisLabelText": "",
        "yAxisLabelText": "",
        "sort": {
            "directionD0": "labelAscending",
            "directionD1": "labelAscending"
        },
        "zoom": False,
        "explodeSlices": False,
        "showOtherGroup": True,
        "chartType": "verticalBar",
        "colorScheme": "flame"
    },
    "statsDrillin": False
}.items())


class StatsReport(Report):
    """A stats report class used for searching."""

    def __init__(self, fields):
        """Init a StatsReport."""
        self._fields = fields

    @classmethod
    def new_for(cls, app_id, user_id, name):
        """Get a prefilled StatsReport for the App designated by app_id.

        Args:
            app_id (str): The ID of the App to search in.
            user_id (str): The ID of the user creating the report.
            name (str): The name of the Report.

        Return:
            A prefilled StatsReport.
        """
        report = super(StatsReport, cls).new_for(app_id, user_id, name)
        fields = list(report._fields.items())
        return StatsReport(SwimlaneDict(dict(fields + TEMPLATE)))

    @classmethod
    def find_all(cls, app_id=None):
        """Find all stats reports.

        If app_id is specified, only reports that are a member of that App
        will be returned. By default, all reports in the system are returned.

        Args:
            app_id (str): An App ID.

        Returns:
            A generator that yields StatsReports.
        """
        parent_all = super(StatsReport, cls).find_all(app_id)
        return (StatsReport(r._fields) for r in parent_all
                if "StatsReport" in r._fields["$type"])

