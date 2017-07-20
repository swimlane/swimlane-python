import pendulum

from swimlane.core.cursor import PaginatedCursor
from swimlane.core.resources.base import APIResource
from swimlane.core.search import CONTAINS, EQ, EXCLUDES, NOT_EQ


class Report(APIResource, PaginatedCursor):
    """A report class used for searching

    Can be iterated over to retrieve results

    Notes:
        Record retrieval is lazily evaluated and cached internally, adding a filter and attempting to iterate again will
        not respect the additional filter and will return the same set of records each time

    Examples:

        Lazy retrieval of records with direct iteration over report

        ::

            report = app.reports.build('new-report')
            report.filter('field_1', 'equals', 'value')

            for record in report:
                do_thing(record)

        Full immediate retrieval of all records

        ::

            report = app.reports.build('new-report')
            report.filter('field_1', 'doesNotEqual', 'value')

            records = list(report)


    Attributes:
        name (str): Report name
    """

    _type = "Core.Models.Search.Report, Core"

    _FILTER_OPERANDS = (
        EQ,
        NOT_EQ,
        CONTAINS,
        EXCLUDES
    )

    default_limit = 50

    def __init__(self, app, raw, limit=default_limit):
        APIResource.__init__(self, app._swimlane, raw)
        PaginatedCursor.__init__(self, limit=limit)

        self.name = self._raw['name']

        self._app = app

    def __str__(self):
        return self.name

    def _retrieve_raw_elements(self, page):
        body = self._raw.copy()

        body['pageSize'] = self.page_size
        body['offset'] = page

        response = self._swimlane.request('post', 'search', json=body)
        return response.json()['results'].get(self._app.id, [])

    def _parse_raw_element(self, raw_element):
        return self._app.records.get(id=raw_element['id'])

    def filter(self, field_name, operand, value):
        """Adds a filter to report

        Notes:
            All filters are currently AND'ed together

        Args:
            field_name (str): Target field name to filter on
            operand (str): Operand used in comparison. See `swimlane.core.search` for options
            value: Target value used in comparision
        """
        if operand not in self._FILTER_OPERANDS:
            raise ValueError('Operand must be one of {}'.format(', '.join(self._FILTER_OPERANDS)))

        self._raw['filters'].append({
            "fieldId": self._app.get_field_definition_by_name(field_name)['id'],
            "filterType": operand,
            "value": value
        })


def report_factory(app, report_name, limit=Report.default_limit):
    """Report instance factory populating boilerplate raw data"""
    # pylint: disable=protected-access
    created = pendulum.now().to_rfc3339_string()
    user_model = app._swimlane.user.get_usergroup_selection()

    return Report(
        app,
        {
            "$type": Report._type,
            "groupBys": [],
            "aggregates": [],
            "applicationIds": [app.id],
            "columns": [],
            "sorts": {
                "$type": "System.Collections.Generic.Dictionary`2"
                         "[[System.String, mscorlib],"
                         "[Core.Models.Search.SortTypes, Core]], mscorlib",
            },
            "filters": [],
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
            "name": report_name,
            "disabled": False,
            "keywords": ""
        },
        limit=limit
    )
