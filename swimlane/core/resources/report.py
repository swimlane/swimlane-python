"""This module provides a Report class."""

from datetime import datetime

from swimlane.core.resources.base import APIResourceAdapter, APIResource


class ReportAdapter(APIResourceAdapter):

    _page_size = 20

    def __init__(self, app):
        super(ReportAdapter, self).__init__(app.swimlane)

        self.app = app

    def list(self):
        """Retrieve all reports

        If app is specified, only reports that are a member of that App
        will be returned. By default, all reports in the system are returned.
        """
        raw_reports = self.swimlane.api('get', "reports?appId={}".format(self.app.id)).json()
        results = []
        for raw_report in raw_reports:
            try:
                results.append(Report(self.app, raw_report))
            except TypeError:
                # Ignore StatsReports for now
                pass

        return results

    def get(self, report_id):
        """Retrieve report by ID"""
        return Report(
            self.app,
            self.swimlane.api('get', "reports/{0}".format(report_id))
        )

    def new(self, name):
        """Get a new Report for the App designated by app_id.

        Args:
            app (str): The App or app id to search in.
            name (str): The name of the Report.

        Return:
            A prefilled Report.
        """
        created = datetime.utcnow().isoformat() + "Z"
        user_model = self.swimlane.user.get_user_selection()

        return Report(self.app, {
            "$type": Report._type,
            "groupBys": [],
            "aggregates": [],
            "applicationIds": [self.app.id],
            "columns": [f['id'] for f in self.app.fields],
            "sorts": {
                "$type": "System.Collections.Generic.Dictionary`2"
                         "[[System.String, mscorlib],"
                         "[Core.Models.Search.SortTypes, Core]], mscorlib",
            },
            "filters": [],
            "pageSize": self._page_size,
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


class Report(APIResource):
    """A report class used for searching."""

    _type = "Core.Models.Search.Report, Core"

    EQ = "equals"
    NOT_EQ = "doesNotEqual"
    CONTAINS = "contains"
    EXCLUDES = "excludes"

    _OPERANDS = (
        EQ,
        NOT_EQ,
        CONTAINS,
        EXCLUDES
    )

    def __init__(self, app, raw):
        super(Report, self).__init__(app.swimlane, raw)

        self.app = app

    def save(self):
        """Insert the current Report."""
        return
        '''if insert:
            self._fields = self.swimlane.api('post', "reports")
        else:
            self._fields = self.swimlane.api('put', "reports")'''

    def add_filter(self, field, operand, value):
        """Returns a filter object from field name, comparision operand and value"""
        if operand not in self._OPERANDS:
            raise ValueError('Operand must be one of {}'.format(', '.join(self._OPERANDS)))

        self._raw['filters'].append({
            "fieldId": self.app.get_field_id(field),
            "filterType": operand,
            "value": value,
        })

    def delete(self):
        raise NotImplementedError

    def run(self):
        # Avoid circular imports
        from swimlane.core.resources import Record
        report_data = self.swimlane.api('post', 'search', json=self._raw).json()

        results = report_data['results'].get(self.app.id, [])

        return [Record(self.app, raw_record) for raw_record in results]

