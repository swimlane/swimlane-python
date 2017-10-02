.. _resource-examples:


Resources
=========

See :mod:`swimlane.core.resources` for full API docs on all resources





App
---

App instances represent apps available on Swimlane server, and provide methods to retrieve and create child Records

Retrieve apps using the `apps` adapter available on the :class:`swimlane.Swimlane` client


Retrieve Records
^^^^^^^^^^^^^^^^

Records can be retrieved by full IDs. Only records in the source app are returned, IDs matching records from other apps
will fail to be retrieved.

.. code-block:: python

    record = app.records.get(id='58f...387')


Search Records
^^^^^^^^^^^^^^

Searching is done using the :obj:`app.records` adapter, and uses temporary :class:`~swimlane.core.resources.report.Report`
instances to handle paginated search results and record retrieval on-demand.

Filters can be applied using tuples of `(<field_name>, <filter_operator>, <field_value>)` that will be AND'ed together
on the report.

.. code-block:: python

    records = app.records.search(
        ('Text Field', 'equals', 'value'),
        ('Date Field', 'lessThan', pendulum.now()),
        ('Values List (Multi-Select)', 'equals', ['Option 1', 'Option 2'])
        ('Reference (Single-Select)', 'equals', target_record)
    )

Keyword-searches can be performed by providing a `keywords` list parameter. All records with fields matching the
provided keywords will be returned

.. code-block:: python

    records = app.records.search(
        keywords=[
            'target',
            'keywords'
        ]
    )

Available operators are just strings as shown above, but are made available as constants in the
:mod:`~swimlane.core.search` module

.. code-block:: python

    from swimlane.core.search import EQ, NOT_EQ, CONTAINS, EXCLUDES, GT, LT, GTE, LTE

    records = app.records.search(
        ('Text Field', EQ, 'equal value'),
        ('Number Field', GTE, 0),
    )

.. warning::

    Report results are retrieved during on-demand during iteration, requesting record data from the API before each loop
    to improve performance and reduce memory footprint.

    Using :obj:`app.records.search` loads all records into a list before returning, which can be an expensive
    operation, especially with many results.

    A default limit of 50 records is placed on all reports for performance, use the :obj:`limit` parameter to
    override the default limit on a search, a limit of `0` retrieves all search results.

    .. code-block:: python

        # retrieve all results
        records = app.records.search(
            ('Text Field', 'equals', 'value'),
            ...
            limit=0
        )

To operate on large search results as records are returned from API or retrieve only partial results
:class:`~swimlane.core.resources.report.Report` should be used instead.

.. code-block:: python

    report = app.reports.build('report-name', limit=0)

    # Apply report filters
    # These work like search filters, but must be applied one-by-one and are NOT tuples like in app.records.search()
    report.filter('Text Field', 'equals', 'value')
    report.filter('Numeric Field', 'equals', 0)

    # Each record is retrieved from the API on-demand before each iteration
    for record in report:

        # Do something with each retrieved record
        record['Test Field'] = 'modified'

        if some_condition:
            # No additional records will be retrieved from report after breaking out of loop
            break

    # Report results are cached after first iteration, will not make additional requests or retrieve any skipped results
    # Any modifications to records from report are maintained
    for record in report:
        assert record['Test Field'] == 'modified'



Create New Record
^^^^^^^^^^^^^^^^^

Record creation is done through the :obj:`app.records` adapter, and adheres to all field validation as documented below

The newly created record is returned from the create create call after first being persisted on the server

.. code-block:: python

    new_record = app.records.create(**{
        'Text Field': 'Field Value',
        'Numeric Field': 50,
        ...
    })


Batch Record Creation
^^^^^^^^^^^^^^^^^^^^^

Creating multiple records at once can also done withe the :obj:`app.records` adapter using only a single request.

Any records not passing validation will cause the entire operation to fail.

.. code-block:: python

    records = app.records.create_batch(
        {'Text Field': 'Value 1', 'Numeric Field': 10, ...},
        {'Text Field': 'Value 2', 'Numeric Field': 20, ...},
        ...
    )




Record
------

Record instances represent individual records inside a corresponding app on Swimlane server.

They provide the ability to interact with field data similar to how it's done in the Swimlane UI, and handle translating
and validating field types using various :class:`~swimlane.core.fields.base.field.Field` classes under the hood.


Accessing Field Values
^^^^^^^^^^^^^^^^^^^^^^

Fields are accessed as keys by their readable field names as seen in the UI. Field names are case and whitespace 
sensitive, and are unique within an individual app.

Assuming a record from an app with a text field called "Text" with a value of "Some Example Text", accessing the field
value is done as follows:

.. code-block:: python

    assert record['Text'] == 'Some Example Text'

Any fields without a value default to `None`.


Setting Field Values
^^^^^^^^^^^^^^^^^^^^

Setting field values works the same as accessing values.

.. code-block:: python

    record['Text'] = 'New Text'

    assert record['Text'] == 'New Text'


Clearing Field Values
^^^^^^^^^^^^^^^^^^^^^

Clearing field values can be done in one of two way. The following examples are identical, and simply clear the field
value, setting it back to `None` internally.

.. code-block:: python


    # Delete the field
    del record['Text']

    # Or set directly to None
    record['Text'] = None


Field Validation
^^^^^^^^^^^^^^^^

Most field types enforce a certain type during the set operation, and will raise a
:class:`swimlane.exceptions.ValidationError` on any kind of failure, whether it's an invalid value, incorrect type, etc.
and will contain information about why it was unable to validate the new value.

.. code-block:: python

    try:
        record['Numeric'] = 'String'
    except ValidationError as error:
        print(error)

See :ref:`individual field examples <field-examples>` for more specifics on each field type and their usage.


Saving Changes
^^^^^^^^^^^^^^

All changes to a record are only done locally until explicitly persisted to the server with
:meth:`~swimlane.core.resources.record.Record.save`.

.. code-block:: python

    record['Text'] = 'Some New Text'
    record.save()


Delete Record
^^^^^^^^^^^^^

Records can be deleted from Swimlane using :meth:`~swimlane.core.resources.record.Record.delete`. Record will be
removed from server and marked as a new record, but will retain any field data.

.. code-block:: python

    assert record.tracking_id == 'ABC-123'
    text_field_data = record['Text']

    # Deletes existing record from server
    record.delete()

    assert record.id is None
    assert record['Text'] == text_field_data

    ...

    # Create a new record from the deleted record's field data
    record.save()

    assert record.tracking_id == 'ABC-124'


Field Iteration
^^^^^^^^^^^^^^^

Records can be iterated over like :meth:`dict.items()`, yielding `(field_name, field_value)` tuples

.. code-block:: python

    for field_name, field_value in record:
        assert record[field_name] == field_value


Unknown Fields
^^^^^^^^^^^^^^

Attempting to access a field not available on a record's parent app will raise :class:`swimlane.exceptions.UnknownField`
with the invalid field name, as well as potential similar field names in case of a possible typo.

.. code-block:: python

    try:
        record['Rext'] = 'New Text'
    except UnknownField as error:
        print(error)




UserGroup
---------

Handling Users, Groups, and UserGroups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users and Groups both extend from the base UserGroup class. Most values returned from the server are of the base
UserGroup type, but can be replaced or set by the more specific classes.

.. code-block:: python

    # User / Group fields return UserGroup instances when accessed
    assert type(record['Created By']) is UserGroup

    # But can be set to the more specific User / Group types directly
    record['User'] = swimlane.user
    record['Group'] = swimlane.groups.get(name='Everyone')


Comparisons
^^^^^^^^^^^

Users and Groups and be directly compared to the base UserGroup class, and will be considered equal if the two objects
represent the same entity

.. code-block:: python

    assert record['Created By'] == swimlane.user

    assert record['Group'] == swimlane.groups.get(name='Everyone')
