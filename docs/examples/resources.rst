

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

Searching is done using the :obj:`app.records` adapter, and leverages temporary :class:`~swimlane.core.resources.report.Report`
instances to facilitate search underneath.

Search is done by providing multiple tuples that are applied as filters and AND'ed together on the underlying report.

.. note::

    Reports are normally iterated and paginated over in batches, using the :obj:`records` adapter loads all
    records into a list immediately

.. code-block:: python

    records = app.records.search(
        ('Field Name', 'equals', 'value'),
        ('Other Field', 'doesNotEqual', 'value')
    )


Create New Records
^^^^^^^^^^^^^^^^^^

Record creation is done through the :obj:`app.records` adapter, and adheres to all field validation as documented below

The newly created record is returned from the create create call after first being persisted on the server

.. code-block:: python

    new_record = app.records.create(**{
        'Text Field': 'Field Value',
        'Numeric Field': 50,
        ...
    })


Record
------

Record instances represent individual records inside a corresponding app on Swimlane server.

They provide the ability to interact with field data similar to how it's done in the Swimlane UI, and handle translating
and validating field types using various :class:`~swimlane.core.fields.base.field.Field` classes under the hood.


Getting Field Values
^^^^^^^^^^^^^^^^^^^^

Fields are accessed as keys by their readable field names as seen in the UI.

Assuming a record from an app with a text field called "Text" with a value of "Some Example Text", accessing the field
value is done as follows:

.. code-block:: python

    assert record['Text'] == 'Some Example Text'


Setting Field Values
^^^^^^^^^^^^^^^^^^^^

Setting field values works the same as getting values.

.. code-block:: python

    record['Text'] = 'New Text'
    assert record['Text'] == 'New Text'


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
:meth:`~swimlane.core.resources.record.Record.save`

.. code-block:: python

    record['Text'] = 'Some New Text'
    record.save()


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

