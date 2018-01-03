

Swimlane Client
===============

See :class:`swimlane.core.client.Swimlane` for full client API documentation.



Configuration
-------------

Minimal Setup
^^^^^^^^^^^^^

Bare-minimum values necessary to connect to a Swimlane server with default settings are the `host`, `username`, and
`password`.

Authentication is performed immediately, client instantiation will fail immediately if invalid credentials are provided.

If no scheme is provided, HTTPS is used as the default.

.. code-block:: python

    from swimlane import Swimlane

    swimlane = Swimlane('192.168.1.1', 'username', 'password')


Clear HTTP Connection
^^^^^^^^^^^^^^^^^^^^^

Connecting to Swimlane over plain HTTP is supported, but not recommended.

To connect using HTTP, provide it as part of the host URL.

.. code-block:: python

    from swimlane import Swimlane

    swimlane = Swimlane('http://192.168.1.1', 'username', 'password')


Non-Standard Port
^^^^^^^^^^^^^^^^^

To connect to Swimlane over a non-standard port, include the port as part of the host URL

.. code-block:: python

    from swimlane import Swimlane

    swimlane = Swimlane(
        'https://192.168.1.1:8443',
        'username',
        'password',
        verify_ssl=False
    )


SSL Verification
^^^^^^^^^^^^^^^^

SSL certificate verification is enabled by default for all HTTPS connections. Client instantiation will fail if Swimlane
server SSL certificate cannot be verified.

To disable SSL verification, set `verify_ssl=False` during client instantiation. This will be carried over to all
additional requests made by using the client automatically.

.. warning::

    Because it's common to disable SSL verification, the normal :class:`urllib3.exceptions.InsecureRequestWarning`
    is suppressed automatically when using the Swimlane client. See urllib3_ docs for more information.

.. _urllib3: http://urllib3.readthedocs.io/en/latest/user-guide.html#certificate-verification

.. code-block:: python

    from swimlane import Swimlane

    swimlane = Swimlane(
        '192.168.1.1',
        'username',
        'password',
        verify_ssl=False
    )


The `verify_ssl` parameter is ignored when connecting over HTTP.


Resource Caching
^^^^^^^^^^^^^^^^

.. versionadded:: 2.16.2

The Swimlane client supports automatic caching for most API resources. When enabled, requests for resource data will
first check the client's cache for the requested resource, returning it without making an additional request if found.

To enable caching, set the `resource_cache_size` parameter when initializing the Swimlane client. The cache size applies
to each resource type individually, meaning a cache size of 20 would cause the client to cache up to 20 of each of the
following supported resource types at a time:

- App
- Record
- User
- Group

Once a cache is full, items are removed using "Least Frequently Used (LFU)" priority, meaning the resources that are
most often accessed will be kept in the cache longer than less-frequently accessed resources.

.. code-block:: python

    # Enable basic logging to print requests and cache hits/misses
    import logging; logging.basicConfig(level=logging.DEBUG)

    from swimlane import Swimlane

    # Enable caching up to 20 different instances of each supported resource type
    swimlane = Swimlane(
        '192.168.1.1',
        'username',
        'password',
        resource_cache_size=20
    )

    # Slow code making multiple requests for the same App, Record, and referenced Records in a loop
    # With caching enabled, performance is much higher as requests are sent only for resources not already in the cache
    for _ in range(5):
        app = swimlane.apps.get(id='abc...123')
        print(app)

        record = app.records.get(id='def...456')
        print(record)

        for reference_record in record['Reference Field']:
            print(reference_record)


Resource caching can provide a big performance boost when requesting the same resources multiple times, especially when
performing multiple searches or accessing references fields pointing to the same set of records.


Custom Direct Requests
^^^^^^^^^^^^^^^^^^^^^^

Not all API endpoints may be currently supported by internal adapters, or custom arguments may be required in special
cases not handled by other resources.

To perform a custom request and handle the response directly, use the :meth:`swimlane.Swimlane.request` method.

.. code-block:: python

    from swimlane import Swimlane

    swimlane = Swimlane('192.168.1.1', 'username', 'password')

    response = swimlane.request(
        'post',
        'some/endpoint',
        json={...},
        params={...},
        ...
    )

Underlying connection session will be reused, authentication will be handled automatically, and all default request
configurations will be applied as normal if not provided explicitly.

All provided keyword arguments will be passed to the underlying :meth:`requests.Session.request` call.

.. note::

    Any 400/500 responses will raise :class:`requests.HTTPError` automatically.


Request Timeouts
^^^^^^^^^^^^^^^^

Initial client connection and all request read timeouts are set to 60 seconds by default. For more information on
timeouts, refer to the `Requests timeout documentation`_.

.. _Requests timeout documentation: http://docs.python-requests.org/en/master/user/quickstart/#timeouts

To override the default global timeout used by all library methods, provide the `default_timeout` parameter in seconds
during client instantiation.

.. code-block:: python

    from swimlane import Swimlane

    swimlane = Swimlane(
        '192.168.1.1',
        'username',
        'password',
        default_timeout=300
    )


The :meth:`swimlane.Swimlane.request` method can also accept an optional `timeout` parameter that will override the
global default timeout for the single request.

.. code-block:: python

    from swimlane import Swimlane

    swimlane = Swimlane('192.168.1.1', 'username', 'password')

    # Potentially long delay before starting response with 10 minute timeout
    response = swimlane.request(
        'post',
        'some/endpoint',
        ...,
        timeout=600
    )


Server Version Verification
^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, client will check that the major versions of server and client match, and raise
:class:`swimlane.exceptions.InvalidServerVersion` if they do not.

This may require an additional request that may not otherwise be required to retrieve the server version, and and be
disabled by setting `verify_server_version=False`.

.. note::

    Connecting to a newer major server version is not supported, and should not be expected to work as normal if this
    verification is disabled.

    Only disable this verification when sure you are using the correct client library version.

.. code-block:: python

    from swimlane import Swimlane

    swimlane = Swimlane(
        '192.168.1.1',
        'username',
        'password',
        verify_server_version=False
    )



Available Adapters
------------------

Examples of usage for preconfigured adapters available on client instances, abstracting retrieval and instantiation of
various resource instances.

See various adapter class documentation :mod:`swimlane.core.adapters` for more information

Apps
^^^^

Handles retrieval of App resources.

Retrieve an app by ID or name:

.. code-block:: python

    app_by_id = swimlane.apps.get(id='58f...387')

    app_by_name = swimlane.apps.get(name='Target App')

Get list of all apps:

.. code-block:: python

    apps = swimlane.apps.list()


Users
^^^^^

Handles retrieval of User resources.

Retrieve a single user by ID or display name:

.. code-block:: python

    user_by_id = swimlane.users.get(id='58f...387')

    user_by_display_name = swimlane.users.get(display_name='admin')

Get list of all users:

.. code-block:: python

    users = swimlane.users.list()


Groups
^^^^^^

Handles retrieval of Group resources.

Retrieve a single group by ID or name:

.. code-block:: python

    group_by_id = swimlane.groups.get(id='58f...387')

    group_by_display_name = swimlane.groups.get(name='Everyone')


Get list of all groups:

.. code-block:: python

    groups = swimlane.groups.list()



Helpers
^^^^^^^

Any miscellaneous methods for API endpoints not better suited for other adapters or used for high performance with bulk
requests.

.. code-block:: python

    swimlane.helpers.add_record_references(
        app_id='123...456',
        record_id='789...0ab',
        target_record_ids=[
            '123...456',
            '789...0ab',
            'cde...f12',
            ...
        ]
    )


Check the status of app.records.bulk_modify() or app.records.bulk_delete() jobs.

.. code-block:: python

    # Get target app
    app = swimlane.apps.get(name='App')

    # Bulk modify records matching filters
    job_id = app.records.bulk_modify(
        ('Numeric', 'equals', 1), 
        values={'Numeric': 2}
    )
    
    # Check bulk job status
    status = swimlane.helpers.check_bulk_job_status(job_id)
    print(status)

    [{'$type': 'Core.Models.Jobs.JobInfo, Core',
      'job': 'a4EDVRY7UOHpz5_xV',
      'status': 'started',
      'task': 'BatchRecordUpdate'},
     {'$type': 'Core.Models.Jobs.JobInfo, Core',
      'job': 'a4EDVRY7UOHpz5_xV',
      'message': 'Batch update 100% completed.',
      'status': 'inProgress',
      'task': 'BatchRecordUpdate'},
     {'$type': 'Core.Models.Jobs.JobInfo, Core',
      'details': {'$type': 'Core.Models.Notifications.BulkModifyFinishedNotification, Core',
       'applicationId': 'aRDyEl8ZRd7gKrEN5',
       'bulkModificationType': 'update',
       'dateTime': '2018-01-02T16:46:46.4982709Z',
       'disabled': False,
       'errors': [],
       'id': 'aJxpdAwvKWUSaEPRz',
       'jobId': 'a4EDVRY7UOHpz5_xV',
       'notificationType': 'console',
       'output': 'Task complete',
       'status': 'Finished',
       'taskName': 'BatchRecordUpdate',
       'totalRecordsSkipped': 1,
       'totalRecordsUpdated': 0,
       'userName': 'admin',
       'warnings': [{'$type': 'Core.Models.Notifications.RecordMessage, Core',
         'message': 'Record is already locked, skipping',
         'recordId': 'aPieydMqIo6lgwxd9',
         'trackingId': 'BNAW-15'}]},
      'job': 'a4EDVRY7UOHpz5_xV',
      'status': 'completed',
      'task': 'BatchRecordUpdate'}]
