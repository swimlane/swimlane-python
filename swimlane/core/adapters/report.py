import weakref

import pendulum

from swimlane.core.resolver import SwimlaneResolver
from swimlane.core.resources import Report


class ReportAdapter(SwimlaneResolver):

    def __init__(self, app):
        super(ReportAdapter, self).__init__(app._swimlane)

        self.__ref_app = weakref.ref(app)

    @property
    def _app(self):
        """Resolve weak app reference"""
        return self.__ref_app()

    def list(self):
        """Retrieve all reports

        If app is specified, only reports that are a member of that App
        will be returned. By default, all reports in the system are returned.
        """
        raw_reports = self._swimlane.request('get', "reports?appId={}".format(self._app.id)).json()
        # Ignore StatsReports for now
        return [Report(self._app, raw_report) for raw_report in raw_reports if raw_report['$type'] == Report._type]

    def get(self, report_id):
        """Retrieve report by ID"""
        return Report(
            self._app,
            self._swimlane.request('get', "reports/{0}".format(report_id)).json()
        )

    def build(self, name):
        """Build a new Report for the App designated by app_id"""
        #pylint: disable=protected-access
        created = pendulum.now().to_rfc3339_string()
        user_model = self._swimlane.user.get_usergroup_selection()

        return Report(self._app, {
            "$type": Report._type,
            "groupBys": [],
            "aggregates": [],
            "applicationIds": [self._app.id],
            "columns": list(self._app._fields_by_id.keys()),
            "sorts": {
                "$type": "System.Collections.Generic.Dictionary`2"
                         "[[System.String, mscorlib],"
                         "[Core.Models.Search.SortTypes, Core]], mscorlib",
            },
            "filters": [],
            "pageSize": Report._page_size,
            "offset": 0,
            "defaultSearchReport": False,
            "allowed": [],
            "permissions": {
                "$type": "Core.Models.Security.PermissionMatrix, Core"
            },
            "createdDate": created,
            "modifiedDate": created,
            "createdByUser": user_model,
            "modifiedByUser": user_model,
            "id": None,
            "name": name,
            "disabled": False,
            "keywords": ""
        })
