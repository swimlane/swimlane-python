

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

    swimlane = Swimlane('192.168.1.1', 'username', 'password', verify_ssl=False)


The `verify_ssl` parameter is ignored when connecting over HTTP.


Non-Standard Port
^^^^^^^^^^^^^^^^^

To connect to Swimlane over a non-standard port, include the port as part of the host URL

.. code-block:: python

    from swimlane import Swimlane

    swimlane = Swimlane('https://192.168.1.1:8443', 'username', 'password', verify_ssl=False)


Custom Direct Requests
^^^^^^^^^^^^^^^^^^^^^^

Not all API endpoints may be currently supported by internal adapters, or custom arguments may be required in special
cases not handled by other resources.

To perform a custom request and handle the response directly, use the :meth:`swimlane.Swimlane.request` method.

.. code-block:: python

    from swimlane import Swimlane

    swimlane = Swimlane('192.168.1.1', 'username', 'password')

    response = swimlane.request('post', 'some/endpoint', json={...}, params={...}, ...)

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

To override the default global timeout used by all library methods, provide the `default_timeout` parameter as an
:class:`int` in seconds during client instantiation.

.. code-block:: python

    from swimlane import Swimlane

    swimlane = Swimlane('192.168.1.1', 'username', 'password', default_timeout=300)


The :meth:`swimlane.Swimlane.request` method can also accept an optional `timeout` parameter that will override the
global default timeout for the single request.

.. code-block:: python

    from swimlane import Swimlane

    swimlane = Swimlane('192.168.1.1', 'username', 'password')

    # Potentially long-running request
    response = swimlane.request('post', 'some/endpoint', ..., timeout=600)




Available Adapters
------------------

Examples of usage for preconfigured adapters available on client instances, abstracting retrieval and instantiation of
various resource instances.

See various adapter class documentation :mod:`swimlane.core.adapters` for more information

Apps
^^^^

Retrieve an app by ID or name:

.. code-block:: python

    app_by_id = swimlane.apps.get(id='58f...387')

    app_by_name = swimlane.apps.get(name='Target App')

Get list of all apps:

.. code-block:: python

    users = swimlane.users.list()


Users
^^^^^

Retrieve a single user by ID or display name:

.. code-block:: python

    user_by_id = swimlane.users.get(id='58f...387')

    user_by_display_name = swimlane.users.get(display_name='admin')

Get list of all users:

.. code-block:: python

    users = swimlane.users.list()


Groups
^^^^^^

Retrieve a single group by ID or name:

.. code-block:: python

    group_by_id = swimlane.groups.get(id='58f...387')

    group_by_display_name = swimlane.groups.get(name='Everyone')


Get list of all groups:

.. code-block:: python

    users = swimlane.groups.list()

