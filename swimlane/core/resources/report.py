import pendulum
import json 


from swimlane.core.cursor import PaginatedCursor
from swimlane.core.fields.list import ListField
from swimlane.core.resources.base import APIResource
from swimlane.core.resources.record import Record, record_factory
from swimlane.core.search import CONTAINS, EQ, EXCLUDES, NOT_EQ, LT, GT, LTE, GTE, ASC, DESC
from swimlane.utils import validate_type

ALLOWED_OPERATORS = ['Or', 'And']


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

    _type = "Core.Models.Search.StatsReport, Core"

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
    default_page_start = None
    default_page_end = None

    def __init__(self, app, raw, **kwargs):
        APIResource.__init__(self, app._swimlane, raw)
        PaginatedCursor.__init__(self,
                                 limit=kwargs.pop('limit', self.default_limit),
                                 page_size=kwargs.pop('page_size', self.default_page_size),
                                 page_start=kwargs.pop('page_start', self.default_page_start),
                                 page_end=kwargs.pop('page_end', self.default_page_end)
                                 )

        self.name = self._raw['name']
        self.keywords = kwargs.pop('keywords', [])

        self._app = app

        for field_id in self._app._fields_by_id.keys():
            self._raw['columns'].append(field_id)

    def filter_type(self, filter_type):
        filter_type = filter_type.capitalize()
        self.validateOperator(filter_type)
        self.filter_type = filter_type

    def validateOperator(self, operator):
        if operator not in ALLOWED_OPERATORS:
            raise ValueError('filter_type value not allowed')

    def __str__(self):
        return self.name

    def _retrieve_raw_elements(self, page):
        body = self._raw.copy()

        body['pageSize'] = self.page_size
        body['offset'] = page
        if(type(self.filter_type) is str):
            body['filterType'] = self.filter_type
        body['keywords'] = ', '.join(self.keywords)

        response = self._swimlane.request('post', 'search', json=body)
        return response.json()['results'].get(self._app.id, [])

    def _parse_raw_element(self, raw_element):
        return Record(self._app, raw_element)

    def get_raw_json(self):
        """Get raw JSON data for all search results without converting to Record objects.
        
        This method is intended for troubleshooting and integration with external systems
        that work with raw JSON data rather than parsed Record objects. It provides access to
        the original JSON response data from the search API before any object conversion,
        field parsing, or validation.
        
        The method will trigger data retrieval if not already performed, but returns
        the raw JSON elements instead of the parsed Record instances.
        
        Returns:
            list: List of raw JSON dictionaries representing each search result
            
        Examples:
            # Get raw JSON for troubleshooting search results
            report = app.reports.build('my-report')
            report.filter('Status', 'equals', 'Open')
            raw_data = report.get_raw_json()
            
            # Inspect the raw structure to understand field mappings
            if raw_data:
                print("Raw JSON structure:", raw_data[0].keys())
                print("Available field values:", raw_data[0].get('values', {}).keys())
                
            # Export to external system expecting JSON format
            import json
            with open('search_results.json', 'w') as f:
                json.dump(raw_data, f, indent=2)
                
            # Process raw field data for integration
            for raw_record in raw_data:
                field_values = raw_record.get('values', {})
                # Process field_values dict directly without Record object overhead
                external_system.process(field_values)
                
        Notes:
            - This method will evaluate the search if not already done
            - Raw data is cached after first retrieval for performance
            - Useful for debugging field mappings and API response structure
            - Essential for integrations with systems that expect raw JSON format
            - Bypasses all Record object creation, field validation, and type conversion
            - Field values are in their raw API format (e.g., field IDs as keys)
        """
        # Store raw elements during evaluation
        raw_elements = []
        
        # Determine pagination range based on parameters (copied from PaginatedCursor logic)
        if self.page_start and self.page_end:
            page_range = range(self.page_start-1, self.page_end)
        elif self.page_start:
            import itertools
            page_range = itertools.count(self.page_start-1)
        elif self.page_end:
            page_range = range(0, self.page_end)
        else:
            import itertools
            page_range = itertools.count()

        # Retrieve raw data page by page
        for page in page_range:
            page_raw_elements = self._retrieve_raw_elements(page)
            
            for raw_element in page_raw_elements:
                raw_elements.append(raw_element)
                
                # Respect limit if set
                if hasattr(self, '_PaginatedCursor__limit') and self._PaginatedCursor__limit and len(raw_elements) >= self._PaginatedCursor__limit:
                    break

            # Break conditions for ending pagination
            if any([
                len(page_raw_elements) < self.page_size,
                hasattr(self, '_PaginatedCursor__limit') and self._PaginatedCursor__limit and len(raw_elements) >= self._PaginatedCursor__limit,
                self.page_size == 0
            ]):
                break
        
        return raw_elements

    def filter(self, field_name, operand, value):
        """Adds a filter to report

        Notes:
            1. All filters are currently AND'ed together.
            2. None values work like a wildcard and will skip type verification.

        Args:
            field_name (str): Target field name to filter on
            operand (str): Operand used in comparison. See `swimlane.core.search` for options
            value: Target value used in comparison
        """
        if operand not in self._FILTER_OPERANDS:
            raise ValueError('Operand must be one of {}'.format(', '.join(self._FILTER_OPERANDS)))

        field = self._get_stub_field(field_name)
        
        validate_type(field, value)

        value = self.parse_field_value(field, value)

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
        if not field_name or not isinstance(field_name, str):
            raise ValueError('field_name is of an invalid format, expected non-empty string')

        # Use temp Record instance for target app to translate values into expected API format
        record_stub = record_factory(self._app)
        return record_stub.get_field(field_name)

    def parse_field_value(self, field, value):
        if isinstance(field, ListField):
            type = self.get_field_list_type(field.input_type)
            value = self.get_default_value(value, field.input_type)
        if isinstance(field, ListField) and not isinstance(value, list) and value is not None:
            self.validate_type(value, type, field.input_type)
            return [value]
        elif isinstance(field, ListField) and isinstance(value, list) and any(not isinstance(elem, type) for elem in value):
            raise TypeError('Field item must be a {}.'.format(field.input_type))
        return value

    def validate_type(self, value, type, type_name=None):
        if(not type_name):
            type_name = type
        if not isinstance(value, type):
            raise TypeError('Field must be a {}.'.format(type_name))
        
    def get_default_value(self, value, field_type):
        if(value == '' and field_type == 'text'):
            value = None
        return value

    def get_field_list_type(self, field_type):
        if field_type == 'text':
            return str
        elif field_type == 'numeric':
            return (int, float)

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
