import weakref

import six

from swimlane.core.resolver import SwimlaneResolver
from swimlane.core.resources.record import Record, record_factory
from swimlane.utils import random_string, one_of_keyword_only


class RecordAdapter(SwimlaneResolver):
    """Handles retrieval and creation of Swimlane Record resources"""

    def __init__(self, app):
        super(RecordAdapter, self).__init__(app._swimlane)

        self.__ref_app = weakref.ref(app)

    @property
    def _app(self):
        """Resolve app weak reference"""
        return self.__ref_app()

    @one_of_keyword_only('id')
    def get(self, _, value):
        """Get a single record by id

        Keyword Args:
            id (str): Full record ID

        Returns:
            Record: Matching Record instance returned from API

        Raises:
            TypeError: No id argument provided
        """
        response = self._swimlane.request('get', "app/{0}/record/{1}".format(self._app.id, value))
        return Record(self._app, response.json())

    def search(self, *filter_tuples):
        """Shortcut to generate a new temporary search report using provided filters and return the resulting records

        Notes:
            Uses a temporary Report instance with a random name to facilitate search. Records are normally paginated,
            but are returned as a single list here, potentially causing performance issues with large searches.

            All provided filters are AND'ed together

            Filter operators are available as constants in `swimlane.core.search`

        Examples:

            ::

                records = app.records.search(
                    ('field_name', 'equals', 'field_value'),
                    ('other_field', search.NOT_EQ, 'value')
                )

        Returns:
            :class:`list` of :class:`~swimlane.core.resources.record.Record`: List of Record instances returned from the
                search results
        """
        report = self._app.reports.build('search-' + random_string(8))

        for filter_tuple in filter_tuples:
            report.filter(*filter_tuple)

        return list(report)

    def create(self, **fields):
        """Create and return a new record in associated app and return the corresponding Record instance
        
        Notes:
            Keyword arguments should be field names with their respective python values

        Examples:
            Create a new record on an app with simple field names

            >>> record = app.records.create(field_a='Some Value', someOtherField=100, ...)

            Create a new record on an app with complex field names

            >>> record = app.records.create(**{'Field 1': 'Field 1 Value', 'Other Field': 100, ...})

        Returns:
            Record: Newly created Record instance with data as returned from API response

        Raises:
            swimlane.exceptions.UnknownField: Raised if any fields are provided that are not available on target app
        """
        # Use temporary Record instance to build fields and inject python values
        new_record = record_factory(self._app)

        for field_name, field_value in six.iteritems(fields):
            new_record[field_name] = field_value

        new_record.save()

        return new_record
