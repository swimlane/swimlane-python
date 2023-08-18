import six

from swimlane.core.bulk import Replace, _BulkModificationOperation
from swimlane.core.cache import check_cache
from swimlane.core.resolver import AppResolver
from swimlane.core.resources.record import Record, record_factory
from swimlane.core.resources.report import Report
from swimlane.utils import random_string, one_of_keyword_only, validate_type
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
            ValueError: The lookup value is empty or None
        """

        if not value:
            raise ValueError('The value provided for the key "{0}" cannot be empty or None'.format(key))

        if key == 'id':
            response = self._swimlane.request('get', "app/{0}/record/{1}".format(self._app.id, value))
            return Record(self._app, response.json())
        if key == 'tracking_id':
            response = self._swimlane.request('get', "app/{0}/record/tracking/{1}".format(self._app.id, value))
            return Record(self._app, response.json())

    def search(self, *filters, filter_type = 'And', **kwargs):
        """Shortcut to generate a new temporary search report using provided filters and return the resulting records

        Args:
            *filters (tuple): Zero or more filter tuples of (field_name, operator, field_value)

        Keyword Args:
            keywords (list(str)): List of strings of keywords to use in report search
            limit (int): Set maximum number of returned Records, defaults to `Report.default_limit`. Set to 0 to return
                all records
            page_size: Set maximum number of returned Records per page, defaults to 1000.
                Set to 0 to return all records
            sort: Tuple of (field_name, order) by which results will be sorted
            columns (list(str)): List of strings of field names to populate in the resulting records. Defaults to all
                available fields

        Notes:
            Uses a temporary Report instance with a random name to facilitate search. Records are normally paginated,
            but are returned as a single list here, potentially causing performance issues with large searches.

            All provided filters are AND'ed together

            Filter operators and sort orders are available as constants in `swimlane.core.search`

        Examples:

            ::

                # Return records matching all filters with default limit and page size

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

            ::

                # Populate only the specified field and sort results
                records = app.records.search(columns=['field_name'], sort=('field_name', 'ascending'))


        Returns:
            :class:`list` of :class:`~swimlane.core.resources.record.Record`: List of Record instances returned from the
                search results
        """
        report = self._app.reports.build(
            'search-' + random_string(8),
            keywords=kwargs.pop('keywords', []),
            limit=kwargs.pop('limit', Report.default_limit),
            page_size=kwargs.pop('page_size', 1000),
            page_start=kwargs.pop('page_start', None),
            page_end=kwargs.pop('page_end', None)
        )

        for filter_tuples in filters:
            report.filter(*filter_tuples)

        sort_tuple = kwargs.pop('sort', None)
        if sort_tuple:
            report.sort(*sort_tuple)

        columns = kwargs.pop('columns', None)
        if columns:
            report.set_columns(*columns)
        
        report.filter_type(filter_type)     

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

        return self._swimlane.request(
            'post',
            'app/{}/record/batch'.format(self._app.id),
            json=[r._raw for r in new_records]
        ).json()

    # pylint: disable=too-many-branches
    @requires_swimlane_version('2.17')
    def bulk_modify(self, *filters_or_records_or_ids, **kwargs):
        """Shortcut to bulk modify records
        
        .. versionadded:: 2.17.0
        
        Args:
            *filters_or_records_or_ids (tuple), (Record), or (string): a list of Records, a list of recordIds, a list of filters, or a list of both records and recordIds.

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

                # Using recordIds
                app.records.bulk_modify("adtDzpdDRv9zM8C4o", "aHlAFdBBjE020Jrzb", "aAR67lIcEnLknaURw", values={"Field Name": "New Value"})

                # Bulk modify by mixing record instances and record ids
                record1 = app.records.get(tracking_id='APP-1')
                app.records.bulk_modify(record1, "aHlAFdBBjE020Jrzb", "aAR67lIcEnLknaURw", values={"Field Name": "New Value"})

        Returns:
            :class:`string`: Bulk Modify Job ID
        """
        values = kwargs.pop('values', None)

        if kwargs:
            raise ValueError('Unexpected arguments: {}'.format(kwargs))

        if not values:
            raise ValueError('Must provide "values" as keyword argument')

        if not isinstance(values, dict):
            raise ValueError('values parameter must be dict of {"field_name": "update_value"} pairs')

        _type = validate_filters_or_records_or_ids(filters_or_records_or_ids)

        request_payload = {}
        record_stub = record_factory(self._app)

        if _type is Record or _type is str:
            the_record_ids = []
            for record_or_id in filters_or_records_or_ids:
                if isinstance(record_or_id, Record):
                    the_record_ids.append(record_or_id.id)
                else:
                    the_record_ids.append(record_or_id)

            request_payload["recordIds"] = [item for item in the_record_ids]

        # build filters
        else:
            filters = []
            for filter_tuples in filters_or_records_or_ids:
                field_name = record_stub.get_field(filter_tuples[0])

                value = filter_tuples[2]
                validate_type(field_name, value)

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
                raise ValueError('Field "{}" of Type "{}", is not supported for bulk modify'.format(
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
        if _type is Record or _type is str:
            for record in filters_or_records_or_ids:
                # if value is an ID, get the record instance
                if type(record) is str:
                    record = self.get(id=record)
                for field_name, modification_operation in six.iteritems(values):
                    record[field_name] = modification_operation.value

        return response.text






    @requires_swimlane_version('2.17')
    def bulk_delete(self, *filters_or_records_or_ids):
        """Shortcut to bulk delete records
        
        .. versionadded:: 2.17.0
        
        Args:
            *filters_or_records_or_ids (tuple) or (Record): Either a list of Records, a list of filters, a list of recordIds, or a list of both records and recordIds.
            
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

                # Bulk delete by record ids
                app.records.bulk_delete("adtDzpdDRv9zM8C4o", "aHlAFdBBjE020Jrzb", "aAR67lIcEnLknaURw", values={"Field Name": "New Value"})

                # Bulk delete by mixing record instances and record ids
                record1 = app.records.get(tracking_id='APP-1')
                app.records.bulk_delete(record1, "aHlAFdBBjE020Jrzb", "aAR67lIcEnLknaURw", values={"Field Name": "New Value"})

        Returns:
            :class:`string`: Bulk Modify Job ID
        """

        _type = validate_filters_or_records_or_ids(filters_or_records_or_ids)
        data_dict = {}

        # build record_id list
        if _type is Record or _type is str:
            record_ids = []
            for item in filters_or_records_or_ids:
                if isinstance(item, Record):
                    record_ids.append(item.id)
                else:
                    record_ids.append(item)
            data_dict['recordIds'] = record_ids

        # build filters
        else:
            filters = []
            record_stub = record_factory(self._app)
            for filter_tuples in filters_or_records_or_ids:
                field = record_stub.get_field(filter_tuples[0])

                value = filter_tuples[2]
                validate_type(field, value)

                filters.append({
                    "fieldId": field.id,
                    "filterType": filter_tuples[1],
                    "value": field.get_report(filter_tuples[2])
                })
            data_dict['filters'] = filters

        return self._swimlane.request('DELETE', "app/{0}/record/batch".format(self._app.id), json=data_dict).text


def validate_filters_or_records_or_ids(filters_or_records_or_ids):
    """Validation for filters_or_records variable from bulk_modify and bulk_delete"""
    # If filters_or_records_or_ids is empty, fail
    if not filters_or_records_or_ids:
        raise ValueError('Must provide at least one filter tuples, Records, or list of Ids')

    _types = [type(item) for item in filters_or_records_or_ids]

    types_dict = {
        "record": 0,
        "str": 0,
        "tuple": 0
    }

    for _type in _types:
        if _type is tuple:
            types_dict["tuple"] = types_dict["tuple"] + 1
        elif _type is Record:
            types_dict["record"] = types_dict["tuple"] + 1
        elif _type is str:
            types_dict["str"] = types_dict["tuple"] + 1
        else:
            raise ValueError('Expected filter tuple, Record, or string, received {0}'.format(_type))

    if types_dict["tuple"] > 0 and (types_dict["record"] > 0 or types_dict["str"] > 0):
        raise ValueError('Cannot mix filter tuples with records or ids')

    # either all tuples or a mix of record and str, which is handled together
    return _types[0]
