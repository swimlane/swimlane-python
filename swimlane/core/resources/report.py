import pendulum

from swimlane.core.cursor import PaginatedCursor
from swimlane.core.resources.base import APIResource
from swimlane.core.resources.record import Record, record_factory
from swimlane.core.search import CONTAINS, EQ, EXCLUDES, NOT_EQ, LT, GT, LTE, GTE, ASC, DESC


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

    Keyword Args:
        limit (int): Max number of records to return from report/search
        page_size (int): Max number of records per page
        keywords (list(str)): List of keywords to use in report/search
    """

    _type = "Core.Models.Search.Report, Core"

    _FILTER_OPERANDS = (
        EQ,
        NOT_EQ,
        CONTAINS,
        EXCLUDES,
        LT,
        GT,
        LTE,
        GTE
    )

    _SORT_ORDERS = (
        ASC,
        DESC
    )

    default_limit = 50

    def __init__(self, app, raw, **kwargs):
        APIResource.__init__(self, app._swimlane, raw)
        PaginatedCursor.__init__(self,
                                 limit=kwargs.pop('limit', self.default_limit),
                                 page_size=kwargs.pop('page_size', self.default_page_size))

        self.name = self._raw['name']
        self.keywords = kwargs.pop('keywords', [])

        self._app = app

        for field_id in self._app._fields_by_id.keys():
            self._raw['columns'].append(field_id)

    def __str__(self):
        return self.name

    def _retrieve_raw_elements(self, page):
        body = self._raw.copy()

        body['pageSize'] = self.page_size
        body['offset'] = page
        body['keywords'] = ', '.join(self.keywords)

        response = self._swimlane.request('post', 'search', json=body)
        return response.json()['results'].get(self._app.id, [])

    def _parse_raw_element(self, raw_element):
        return Record(self._app, raw_element)

    def filter(self, field_name, operand, value):
        """Adds a filter to report

        Notes:
            All filters are currently AND'ed together

        Args:
            field_name (str): Target field name to filter on
            operand (str): Operand used in comparison. See `swimlane.core.search` for options
            value: Target value used in comparison
        """
        if operand not in self._FILTER_OPERANDS:
            raise ValueError('Operand must be one of {}'.format(', '.join(self._FILTER_OPERANDS)))

        field = self._get_stub_field(field_name)

        self._raw['filters'].append({
            "fieldId": field.id,
            "filterType": operand,
            "value": field.get_report(value)
        })

    def sort(self, field_name, order):
        """Adds a sort to report

        Args:
            field_name (str): Target field name to sort by
            order (str): Sort order
        """
        if (order not in self._SORT_ORDERS):
            raise ValueError('Order must be one of {}'.format(', '.join(self._SORT_ORDERS)))

        field = self._get_stub_field(field_name)

        self._raw['sorts'][field.id] = order

    def set_columns(self, *field_names):
        """Set specified columns for report

        Notes:
            The Tracking Id column is always included

        Args:
            *field_names (str): Zero or more column names
        """
        self._raw['columns'] = []
        for field_name in field_names:
            field = self._get_stub_field(field_name)

            self._raw['columns'].append(field.id)

        if self._app.tracking_id not in self._raw['columns']:
            self._raw['columns'].append(self._app.tracking_id)

    def _get_stub_field(self, field_name):
        # Use temp Record instance for target app to translate values into expected API format
        record_stub = record_factory(self._app)
        return record_stub.get_field(field_name)

def report_factory(app, report_name, **kwargs):
    """Report instance factory populating boilerplate raw data

    Args:
        app (App): Swimlane App instance
        report_name (str): Generated Report name

    Keyword Args
        **kwargs: Kwargs to pass to the Report class
    """
    # pylint: disable=protected-access
    created = pendulum.now().to_rfc3339_string()
    user_model = app._swimlane.user.as_usergroup_selection()

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
        **kwargs
    )
