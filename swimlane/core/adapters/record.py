import six

from swimlane.core.bulk import Replace, _BulkModificationOperation
from swimlane.core.cache import check_cache
from swimlane.core.resolver import AppResolver
from swimlane.core.resources.record import Record, record_factory
from swimlane.core.resources.report import Report
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

    def search(self, *filters, **kwargs):
        """Shortcut to generate a new temporary search report using provided filters and return the resulting records

        Args:
            *filters (tuple): Zero or more filter tuples of (field_name, operator, field_value)

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

        for filter_tuples in filters:
            report.filter(*filter_tuples)

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
    def bulk_create(self, *records):
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

                app.records.bulk_create(
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

    # pylint: disable=too-many-branches
    @requires_swimlane_version('2.17')
    def bulk_modify(self, *filters_or_records, **kwargs):
        """Shortcut to bulk modify records
        
        .. versionadded:: 2.17.0
        
        Args:
            *filters_or_records (tuple) or (Record): Either a list of Records, or a list of filters.

        Keyword Args:
            values (dict): Dictionary of one or more 'field_name': 'new_value' pairs to update

        Notes:
            Requires Swimlane 2.17+

        Examples:

            ::

                # Bulk update records by filter

                app.records.bulk_modify(
                    # Query filters
                    ('Field_1', 'equals', value1),
                    ('Field_2', 'equals', value2),
                    ...
                    # New values for records
                    values={
                        "Field_3": value3,
                        "Field_4": value4,
                        ...
                    }
                )

                # Bulk update records

                record1 = app.records.get(tracking_id='APP-1')
                record2 = app.records.get(tracking_id='APP-2')
                record3 = app.records.get(tracking_id='APP-3')

                app.records.bulk_modify(record1, record2, record3, values={"Field_Name": 'new value'})

        Returns:
            :class:`string`: Bulk Modify Job ID
        """
        values = kwargs.pop('values', None)

        if kwargs:
            raise ValueError('Unexpected arguments: {}'.format(kwargs))

        if not values:
            raise ValueError('Must provide "values" as keyword argument')

        if not isinstance(values, dict):
            raise ValueError("values parameter must be dict of {'field_name': 'update_value'} pairs")

        _type = validate_filters_or_records(filters_or_records)

        request_payload = {}
        record_stub = record_factory(self._app)

        # build record_id list
        if _type is Record:
            request_payload['recordIds'] = [record.id for record in filters_or_records]

        # build filters
        else:
            filters = []
            for filter_tuples in filters_or_records:
                field_name = record_stub.get_field(filter_tuples[0])
                filters.append({
                    "fieldId": field_name.id,
                    "filterType": filter_tuples[1],
                    "value": field_name.get_report(filter_tuples[2])
                })
            request_payload['filters'] = filters

        # Ensure all values are wrapped in a bulk modification operation, defaulting to Replace if not provided for
        # backwards compatibility
        for field_name in list(values.keys()):
            modification_operation = values[field_name]
            if not isinstance(modification_operation, _BulkModificationOperation):
                values[field_name] = Replace(modification_operation)

        # build modifications
        modifications = []
        for field_name, modification_operation in values.items():
            # Lookup target field
            modification_field = record_stub.get_field(field_name)
            if not modification_field.bulk_modify_support:
                raise ValueError("Field '{}' of Type '{}', is not supported for bulk modify".format(
                    field_name,
                    modification_field.__class__.__name__
                ))

            modifications.append({
                "fieldId": {
                    "value": modification_field.id,
                    "type": "id"
                },
                "value": modification_field.get_bulk_modify(modification_operation.value),
                "type": modification_operation.type
            })
        request_payload['modifications'] = modifications
        response = self._swimlane.request('put', "app/{0}/record/batch".format(self._app.id), json=request_payload)

        # Update records if instances were used to submit bulk modify request after request was successful
        if _type is Record:
            for record in filters_or_records:
                for field_name, modification_operation in six.iteritems(values):
                    record[field_name] = modification_operation.value

        return response.text

    @requires_swimlane_version('2.17')
    def bulk_delete(self, *filters_or_records):
        """Shortcut to bulk delete records
        
        .. versionadded:: 2.17.0
        
        Args:
            *filters_or_records (tuple) or (Record): Either a list of Records, or a list of filters.
            
        Notes:
            Requires Swimlane 2.17+
            
        Examples:
        
            ::
            
                # Bulk delete records by filter
                app.records.bulk_delete(
                    ('Field_1', 'equals', value1),
                    ('Field_2', 'equals', value2)
                )
                
                # Bulk delete by record instances
                record1 = app.records.get(tracking_id='APP-1')
                record2 = app.records.get(tracking_id='APP-2')
                record3 = app.records.get(tracking_id='APP-3')
                app.records.bulk_delete(record1, record2, record3)

        Returns:
            :class:`string`: Bulk Modify Job ID
        """

        _type = validate_filters_or_records(filters_or_records)
        data_dict = {}

        # build record_id list
        if _type is Record:
            record_ids = []
            for record in filters_or_records:
                record_ids.append(record.id)
            data_dict['recordIds'] = record_ids

        # build filters
        else:
            filters = []
            record_stub = record_factory(self._app)
            for filter_tuples in filters_or_records:
                field = record_stub.get_field(filter_tuples[0])
                filters.append({
                    "fieldId": field.id,
                    "filterType": filter_tuples[1],
                    "value": field.get_report(filter_tuples[2])
                })
            data_dict['filters'] = filters

        return self._swimlane.request('DELETE', "app/{0}/record/batch".format(self._app.id), json=data_dict).text


def validate_filters_or_records(filters_or_records):
    """Validation for filters_or_records variable from bulk_modify and bulk_delete"""
    # If filters_or_records is empty, fail
    if not filters_or_records:
        raise ValueError('Must provide at least one filter tuples or Records')
    # If filters_or_records is not list of Record or tuple, fail
    if not isinstance(filters_or_records[0], (Record, tuple)):
        raise ValueError('Cannot provide both filter tuples and Records')
    # If filters_or_records is not list of either Record or only tuple, fail
    _type = type(filters_or_records[0])
    for item in filters_or_records:
        if not isinstance(item, _type):
            raise ValueError("Expected filter tuple or Record, received {0}".format(item))

    return _type
