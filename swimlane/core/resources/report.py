import itertools

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
        app (App): Parent App instance
        name (str): Report name
    """

    _type = "Core.Models.Search.Report, Core"

    _FILTER_OPERANDS = (
        EQ,
        NOT_EQ,
        CONTAINS,
        EXCLUDES
    )

    _page_size = 50

    def __init__(self, app, raw):
        super(Report, self).__init__(app._swimlane, raw)

        self.app = app
        self.name = self._raw['name']

        self.__records = []

    def __str__(self):
        return self.name

    def __iter__(self):
        """Lazily retrieve and paginate report results and build Record instances from returned data"""
        if self.__records:
            for record in self.__records:
                yield record
        else:
            for page in itertools.count():
                result_data = self._retrieve_report_page(page)
                count = result_data['count']
                records = [self._build_record(raw_data) for raw_data in result_data['results'].get(self.app.id, [])]

                for result in records:
                    self.__records.append(result)
                    yield result

                if not records or len(records) < self._page_size or page * self._page_size >= count:
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
            "fieldId": self.app.get_field_definition_by_name(field_name)['id'],
            "filterType": operand,
            "value": value,
        })

    def _retrieve_report_page(self, page=0):
        """Retrieve paginated report results for an individual page"""
        return self._swimlane.request('post', 'search', json=self._get_paginated_body(page)).json()

    def _build_record(self, raw_record_data):
        # Avoid circular imports
        from swimlane.core.resources import Record
        return Record(self.app, raw_record_data)

    def _get_paginated_body(self, page):
        """Return raw body content formatted with correct pagination and offset values for provided page"""
        body = self._raw.copy()

        body['pageSize'] = self._page_size
        body['offset'] = page

        return body
