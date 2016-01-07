"""This module provides a Report class."""

from datetime import datetime
from ..auth import Client
from .. import SwimlaneDict
from .resource import Resource


class Report(Resource):
    """A report class used for searching."""

    def __init__(self, fields):
        """Init a Report with fields.

        Args:
            fields (dict): A dict of fields and values.
        """
        super(Report, self).__init__(fields)

    def insert(self):
        """Insert the current Report."""
        self._fields = Client.post(self, "reports")

    def update(self):
        """Update the current Report."""
        self._fields = Client.put(self, "reports")

    @classmethod
    def new_for(cls, app_id, user_id, name):
        """Get a prefilled Report for the App designated by app_id.

        Args:
            app_id (str): The ID of the App to search in.
            user_id (str): The ID of the user creating the report.
            name (str): The name of the Report.

        Return:
            A prefilled Report.
        """
        created = datetime.utcnow().isoformat() + "Z"
        return Report(SwimlaneDict({
            "$type": "Core.Models.Search.Report, Core",
            "groupBys": [],
            "aggregates": [],
            "applicationIds": [app_id],
            "columns": [],
            "sorts": {
                "$type": "System.Collections.Generic.Dictionary`2"
                         "[[System.String, mscorlib],"
                         "[Core.Models.Search.SortTypes, Core]], mscorlib",
            },
            "filters": [],
            "pageSize": 18,
            "offset": 0,
            "defaultSearchReport": False,
            "allowed": [],
            "permissions": {
                "$type": "Core.Models.Security.PermissionMatrix, Core"
            },
            "createdDate": created,
            "modifiedDate": created,
            "createdByUser": user_id,
            "modifiedByUser": user_id,
            "id": None,
            "name": name,
            "disabled": False,
            "keywords": ""
        }))

    @classmethod
    def find_all(cls, app_id=None):
        """Find all reports.

        If app_id is specified, only reports that are a member of that App
        will be returned. By default, all reports in the system are returned.
        This method will return either Reports or StatsReports depending on
        what Swimlane returns.

        Args:
            app_id (str): An App ID.

        Returns:
            A generator that yields Reports.
        """
        url = "reports/all"
        if app_id:
            url += "?appId={0}".format(app_id)

        return (Report(r) for r in Client.get(url))

    @classmethod
    def find(cls, report_id):
        """Find a report by ID.

        Args:
            report_id (str): A Report ID.

        Returns:
            A Report.
        """
        return Report(Client.get("reports/{0}".format(report_id)))

