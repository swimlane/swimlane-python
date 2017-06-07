.. _field-examples:

Fields
======

Driver supports all field types available in Swimlane platform with automatic validation and coercion to best
Python representations of field values.


TrackingIdField
---------------

The "Tracking Id" field is always readonly, and exists on all records from all apps

.. code-block:: python

    assert record['Tracking Id'] == 'RA-7'

    try:
        record['Tracking Id'] = 'New Tracking ID'
    except ValidationError:
        assert record['Tracking Id'] == 'RA-7'


TextField
---------

Supports automatic :class:`str` type coercion for non-string types

Assume the example below has a record with a text field "Severity" with the value "7":

.. code-block:: python

    # Coerce to int, add, and automatically set back to str type in field
    assert record['Severity'] == '7'

    # Update value, setting the text field to an int
    record['Severity'] = int(record['Severity']) + 1

    # Value has been coerced to a string
    assert isinstance(record['Severity'], str)
    assert record['Severity'] == '8'


NumericField
------------

Number type enforcement validation. Supports any subclass of :class:`numbers.Number`

.. code-block:: python

    assert isinstance(record['Numeric'], numbers.Number)

    try:
        record['Numeric'] = 'Not a Number'
    except ValidationError:
        record['Numeric'] = 5

    assert record['Numeric'] == 5


DatetimeField
-------------

Full support for all valid Swimlane datetime subtypes:

- Date & Time
- Date
- Time
- Timespan

All datetime values throughout driver are returned as Pendulum_ objects.

.. _Pendulum: https://pendulum.eustace.io/

Fields can be set to appropriate :class:`~datetime.datetime` types or respective :class:`Pendulum` instances, and will
always be converted to corresponding Pendulum type matching the field subtype.

Datetime subtypes (not including Timespan) can be set to full datetime instances, and any extraneous information will be
discarded.

Timezone support is automatic, and can mostly be ignored when using Pendulum instances. All instances returned from
server are set to UTC.


Date & Time
^^^^^^^^^^^

Full specific date & time field

Returns :class:`pendulum.Pendulum` instances

.. code-block:: python

    datetime_field_value = record['Datetime']

    # Drop-in replacement and extension of Python's builtin datetime
    assert isinstance(datetime_field_value, datetime.datetime)
    assert isinstance(datetime_field_value, pendulum.Pendulum)

    assert datetime_field_value.year == 2017
    assert datetime_field_value.month == 4
    assert datetime_field_value.day == 10
    assert datetime_field_value.hour == 16

    # Set to a datetime/pendulum instance
    record['Datetime'] = now = pendulum.now()

    # Fail on generic timestamp/string (not enough context to guarantee consistent behavior)
    try:
        record['Datetime'] = '2017-05-11 11:10:09'
    except ValidationError:
        pass

    assert record['Datetime'] == now


Date
^^^^

Date of year with no time component (2017-06-01).

Returns :class:`pendulum.Date` instances

.. code-block:: python


    date_field = record['Date']
    assert isinstance(date_field, datetime.date)
    assert isinstance(date_field, pendulum.Date)

    # Set to full datetime, time portion is dropped and Date instance is always returned
    record['Date'] = pendulum.now()
    assert isinstance(record['Date'], pendulum.Date)

    # Set to just date
    record['Date'] = pendulum.now().date()
    assert isinstance(record['Date'], pendulum.Date)


Time
^^^^

Time of day with no date component (12:34:56).

Returns :class:`pendulum.Time` instances

.. code-block:: python

    time_field = record['Time']
    assert isinstance(time_field, datetime.time)
    assert isinstance(time_field, pendulum.Time)

    # Set to full datetime, date portion is dropped and Time instance is always returned
    record['Time'] = pendulum.now()
    assert isinstance(record['Time'], pendulum.Time)

    # Set to just time
    record['Time'] = pendulum.now().time()
    assert isinstance(record['Time'], pendulum.Time)


.. warning::

    Time instances do not respect timezone information, and should always be provided in UTC.

    Recommend using full Pendulum datetime instances when working with Time fields. When using full datetimes, the
    timezone is respected before dropping the date portion.


Timespan
^^^^^^^^

Time period (2 hours, 4 minutes, 15 seconds).

Returns :class:`pendulum.Interval` instances

.. code-block:: python

    timespan_field = record['Timespan']
    assert isinstance(timespan_field, datetime.timedelta)
    assert isinstance(timespan_field, pendulum.Interval)


.. note::

    Only subtype that cannot handle datetime/Pendulum instances. Must use datetime.timedelta or pendulum.Interval
    instances instead.


ValuesListField
---------------

Enforces valid selection options available in UI.


Single Select
^^^^^^^^^^^^^

Single-select mode values are accessed and set directly

.. code-block:: python

    # Valid option enforcement
    record['Status'] = 'Open'

    try:
        record['Status'] = 'Not a valid option'
    except ValidationError:
        record['Status'] = 'Closed'

    assert record['Status'] == 'Closed'


Multi Select
^^^^^^^^^^^^

Uses a cursor that behaves similar to a standard list to provide selection functionality and value enforcement.

.. code-block:: python

    # Uses cursor for multi-select support with support for select, deselect, iteration, etc.
    vl_cursor = record['Values List']
    assert len(vl_cursor) == 2

    # Adding the same value multiple times is ignored
    vl_cursor.select('Option 3')
    assert len(vl_cursor) == 3
    vl_cursor.select('Option 3')
    assert len(vl_cursor) == 3

    # Remove element raises exception if not already added
    vl_cursor.deselect('Option 3')
    assert len(vl_cursor) == 2

    try:
        vl_cursor.deselect('Option 3')
    except KeyError:
        assert len(vl_cursor) == 2

    # Respects field's valid options and types, raising ValidationError for invalid values
    try:
        vl_cursor.select('Not a valid option')
    except ValidationError:
        assert len(vl_cursor) == 2

Field can be set directly to any iterable, overwriting current selection entirely

.. code-block:: python

    vl_original_values = list(record['Values List'])

    record['Values List'] = []
    assert len(record['Values List']) == 0

    # All elements must pass validation, or entire set operation fails
    try:
        record['Values List'] = ['Option 1', 'Not a valid option']
    except ValidationError:
        assert len(record['Values List']) == 0

    record['Values List'] = vl_original_values
    assert len(record['Values List']) == 2


UserGroupField
--------------

Returns UserGroup instances (current API limitation)

.. code-block:: python

    usergroup = record['Group']

    assert isinstance(usergroup, UserGroup)
    assert usergroup.id == '58de1d1c07637a0264c0ca71'
    assert usergroup.name == 'Everyone'

    # UserGroup comparisons with specific User/Group instances
    assert usergroup == swimlane.groups.get(name='Everyone')

Set User, Group, or UserGroup

.. code-block:: python


    assert isinstance(swimlane.user, User)

    record['User'] = swimlane.user

    assert record['User'] == swimlane.user

Must be UserGroup instance or extension; Usernames, IDs, display names, etc. are all ambiguous

.. code-block:: python

    record['UserGroup'] = swimlane.user

    try:
        record['UserGroup'] = 'Everyone'
    except ValidationError:
        pass

    assert record['UserGroup'] == swimlane.user

.. note::

    Field support both single-select and multi-select modes like values lists.

    Uses similar cursor as values list for multi-select, works exactly the same but for UserGroup objects instead of
    strings.


AttachmentsField
----------------

Returns a cursor managing iteration existing attachments.

.. code-block:: python

    attachments = record['Attachment']
    assert isinstance(attachments, AttachmentCursor)

    for attachment in attachments:
        # Yields Attachment instances
        assert isinstance(attachment, Attachment)
        assert attachment.filename == '5f09afe50064b2bd718e77818b565df1.pcap'
        assert attachment.file_id == '58ebb22907637a0b488b7b17'
        assert isinstance(attachment.upload_date, datetime)

        # Retrieve file bytes as BytesIO stream (file-like object)
        stream = attachment.download()
        assert isinstance(stream, BytesIO)
        content = stream.read()
        assert len(content) > 0

Upload new attachment with filename and stream or file handle

.. code-block:: python

    attachments = record['Attachment']
    assert len(attachments) == 1

    new_attachment = attachments.add('filename.txt', BytesIO(b'file contents in stream/handle object'))
    assert isinstance(new_attachment, Attachment)
    assert len(attachments) == 2

.. note::

    Attachment is uploaded, and associated with record locally, immediately.

    Association with attachment on server is not persisted until calling :meth:`record.save`.


ReferenceField
--------------

Returns ReferenceCursor with lazy retrieval of target app definition and referenced records as accessed.

Yields (and caches) Record instances when iterated over.

.. note::

    Orphaned referenced records (records deleted but referenced not yet removed) are ignored, and automatically removed
    during iteration.

    Saving a record after iterating over a reference field will remove those orphaned references on the server.

.. code-block:: python

    reference = record['Reference']
    assert isinstance(reference, ReferenceCursor)

    assert len(reference) == 3

    for referenced_record in reference:
        assert isinstance(referenced_record, Record)
        assert referenced_record._app != app
        assert referenced_record._app == reference.target_app

Add or remove references to Records

.. code-block:: python

    other_app = swimlane.apps.get(name='Reference App')
    ref_target_record = other_app.records.get(id='58e24e8607637a0b488849d4')

    # Records added multiple times are ignored
    record['Reference'].add(ref_target_record)
    assert len(record['Reference']) == 4

    record['Reference'].add(ref_target_record)
    assert len(record['Reference']) == 4

    # Remove reference. Raises exception if not already referenced
    record['Reference'].remove(ref_target_record)
    assert len(record['Reference']) == 3

Target app validation

.. code-block:: python

    # Cannot reference a record from an app that is not the reference field's target app
    try:
        record['Reference'].add(record)
    except ValidationError:
        assert len(record['Reference']) == 3

Override all references

.. code-block:: python

    # Can be set to a list of records directly
    # Acts similar to values list, any invalid records cause the entire operation to fail
    record['Reference'] = [ref_target_record]
    assert len(record['Reference']) == 1

    try:
        record['Reference'] = [ref_id, ref_target_record]
    except ValidationError:
        assert len(record['Reference']) == 1


CommentsField
-------------

Cursor managing iteration and addition of comments

.. code-block:: python

    comments = record['Comments']
    assert isinstance(comments, CommentCursor)
    assert len(comments) == 1

    for comment in comments:
        # Yields Comment instances
        assert isinstance(comment, Comment)
        assert isinstance(comment.message, str)
        assert isinstance(comment.user, UserGroup)
        assert isinstance(comment.created_date, datetime)

    # Add new comment
    comments.comment('New comment message')

    # Not persisted until saved, but still listed on local record
    assert len(comments) == 2
    assert comments[1].message == str(comments[1]) == 'New comment message'

.. note::

    Like attachments, comments are associated with a record only locally until calling :meth:`record.save`.


HistoryField
------------

Returns a readonly RevisionCursor object that abstracts out retrieval and pagination of record history

Performs additional request(s) to history API endpoint as accessed

.. code-block:: python

    history = record['History']
    assert isinstance(history, RevisionCursor)

    # Get number of revisions
    num_revisions = len(history)

    # Iterate backwards over revisions
    for idx, revision in enumerate(history):
        assert isinstance(revision, Revision)
        assert isinstance(revision.modified_date, datetime)
        assert isinstance(revision.user, UserGroup)
        assert num_revisions - revision.revision_number == idx

        # revision.version is a full Record instance, and fields can be accessed like a normal Record
        assert revision.version.id == record.id


