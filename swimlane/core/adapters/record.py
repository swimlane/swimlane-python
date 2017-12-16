from swimlane.core.cache import check_cache
from swimlane.core.resolver import AppResolver
from swimlane.core.resources.report import Report
from swimlane.core.resources.record import Record, record_factory
from swimlane.utils import random_string, one_of_keyword_only
from swimlane.utils.version import requires_swimlane_version


class RecordAdapter(AppResolver):
    """Handles retrieval and creation of Swimlane Record resources"""

    @check_cache(Record)
    @one_of_keyword_only('id', 'tracking_id')
    def get(self, key, value):
        """Get a single record by id

        Supports resource cache

        .. versionchanged:: 2.17.0 
            Added option to retrieve record by tracking_id

        Keyword Args:
            id (str): Full record ID
            tracking_id (str): Record Tracking ID

        Returns:
            Record: Matching Record instance returned from API

        Raises:
            TypeError: No id argument provided
        """
        if key == 'id':
            response = self._swimlane.request('get', "app/{0}/record/{1}".format(self._app.id, value))
            return Record(self._app, response.json())
        if key == 'tracking_id':
            response = self._swimlane.request('get', "app/{0}/record/tracking/{1}".format(self._app.id, value))
            return Record(self._app, response.json())

    def search(self, *filter_tuples, **kwargs):
        """Shortcut to generate a new temporary search report using provided filters and return the resulting records

        Args:
            *filter_tuples (tuple): Zero or more filter tuples of (field_name, operator, field_value)

        Keyword Args:
            keywords (list(str)): List of strings of keywords to use in report search
            limit (int): Set maximum number of returned Records, defaults to `Report.default_limit`. Set to 0 to return
                all records

        Notes:
            Uses a temporary Report instance with a random name to facilitate search. Records are normally paginated,
            but are returned as a single list here, potentially causing performance issues with large searches.

            All provided filters are AND'ed together

            Filter operators are available as constants in `swimlane.core.search`

        Examples:

            ::

                # Return records matching all filters with default limit

                from swimlane.core import search

                records = app.records.search(
                    ('field_name', 'equals', 'field_value'),
                    ('other_field', search.NOT_EQ, 'value')
                )

            ::

                # Run keyword search with multiple keywords
                records = app.records.search(keywords=['example', 'test'])

            ::

                # Return all records from app
                records = app.records.search(limit=0)


        Returns:
            :class:`list` of :class:`~swimlane.core.resources.record.Record`: List of Record instances returned from the
                search results
        """
        report = self._app.reports.build(
            'search-' + random_string(8),
            keywords=kwargs.pop('keywords', []),
            limit=kwargs.pop('limit', Report.default_limit)
        )

        for filter_tuple in filter_tuples:
            report.filter(*filter_tuple)

        return list(report)

    def create(self, **fields):
        """Create and return a new record in associated app and return the newly created Record instance

        Args:
            **fields: Field names and values to be validated and sent to server with create request

        Notes:
            Keyword arguments should be field names with their respective python values

            Field values are validated before sending create request to server

        Examples:
            Create a new record on an app with simple field names

            ::

                record = app.records.create(
                    field_a='Some Value',
                    someOtherField=100,
                    ...
                )

            Create a new record on an app with complex field names

            ::

                record = app.records.create(**{
                    'Field 1': 'Field 1 Value',
                    'Field 2': 100,
                    ...
                })

        Returns:
            Record: Newly created Record instance with data as returned from API response

        Raises:
            swimlane.exceptions.UnknownField: If any fields are provided that are not available on target app
            swimlane.exceptions.ValidationError: If any field fails validation before creation
        """
        new_record = record_factory(self._app, fields)

        new_record.save()

        return new_record

    @requires_swimlane_version('2.15')
    def create_batch(self, *records):
        """Create and validate multiple records in associated app

        Args:
            *records (dict): One or more dicts of new record field names and values

        Notes:
            Requires Swimlane 2.15+

            Validates like :meth:`create`, but only sends a single request to create all provided fields, and does not
            return the newly created records

            Any validation failures on any of the records will abort the batch creation, not creating any new records

            Does not return the newly created records

        Examples:
            Create 3 new records with single request

            ::

                app.records.create_batch(
                    {'Field 1': 'value 1', ...},
                    {'Field 1': 'value 2', ...},
                    {'Field 1': 'value 3', ...}
                )

        Raises:
            swimlane.exceptions.UnknownField: If any field in any new record cannot be found
            swimlane.exceptions.ValidationError: If any field in any new record fails validation
            TypeError: If no dict of fields was provided, or any provided argument is not a dict
        """

        if not records:
            raise TypeError('Must provide at least one record')

        if any(not isinstance(r, dict) for r in records):
            raise TypeError('New records must be provided as dicts')

        # Create local records from factory for initial full validation
        new_records = []

        for record_data in records:
            record = record_factory(self._app, record_data)
            record.validate()

            new_records.append(record)

        self._swimlane.request(
            'post',
            'app/{}/record/batch'.format(self._app.id),
            json=[r._raw for r in new_records]
        )
