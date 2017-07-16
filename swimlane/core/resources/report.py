import itertools

import pendulum

from swimlane.core.resources.base import APIResource
from swimlane.core.search import CONTAINS, EQ, EXCLUDES, NOT_EQ


class Report(APIResource):
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

    _page_size = 10
    default_limit = 50

    def __init__(self, app, raw, limit=default_limit):
        super(Report, self).__init__(app._swimlane, raw)

        self.name = self._raw['name']

        self._app = app

        self.__records = []
        self.__limit = limit

        # Cap page size at limit if limit is smaller than a single page
        self._page_size = min(self._page_size, self.__limit)

    def __str__(self):
        return self.name

    def __iter__(self):
        """Lazily retrieve and paginate report results and build Record instances from returned data"""
        if self.__records:
            for record in self.__records:
                yield record
        else:
            for page in itertools.count():
                raw_page_data = self._retrieve_report_page(page)
                count = raw_page_data['count']
                raw_records = raw_page_data['results'].get(self._app.id, [])

                for raw_record in raw_records:
                    record = self._build_record(raw_record)
                    self.__records.append(record)
                    yield record
                    if len(self.__records) >= self.__limit:
                        break

                if any([
                    len(raw_records) < self._page_size,
                    page * self._page_size >= count,
                    len(self.__records) >= self.__limit
                ]):
                    break

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

    def _retrieve_report_page(self, page=0):
        """Retrieve paginated report results for an individual page"""
        return self._swimlane.request('post', 'search', json=self._get_paginated_body(page)).json()

    def _build_record(self, raw_record_data):
        """Retrieve full record as workaround for different report format"""
        return self._app.records.get(id=raw_record_data['id'])

    def _get_paginated_body(self, page):
        """Return raw body content formatted with correct pagination and offset values for provided page"""
        body = self._raw.copy()

        body['pageSize'] = self._page_size
        body['offset'] = page

        return body


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
