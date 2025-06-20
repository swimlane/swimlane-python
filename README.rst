.. image:: https://raw.githubusercontent.com/swimlane/swimlane-python/master/docs/logo.png

Swimlane Python
===============

.. image:: https://img.shields.io/pypi/v/swimlane.svg
    :target: https://pypi.python.org/pypi/swimlane
.. image:: https://img.shields.io/pypi/pyversions/swimlane.svg
    :target: https://pypi.python.org/pypi/swimlane
.. image:: https://travis-ci.org/swimlane/swimlane-python.svg?branch=master
    :target: https://travis-ci.org/swimlane/swimlane-python
.. image:: https://readthedocs.org/projects/swimlane-python-driver/badge/?version=latest
    :target: http://swimlane-python-driver.readthedocs.io/



Python driver for the Swimlane_ API.

.. _Swimlane: http://swimlane.com


.. note::

    This package is compatible with Swimlane 10.x. It is not compatible with Turbine.


------------------------------------------------------------------------------------------

Installation
------------

Install from public repository

::

    pip install swimlane


Or use correct offline installer with bundled dependencies from `releases page`_

.. _releases page: https://github.com/swimlane/swimlane-python/releases

::

    python swimlane-python-offline-installer-<platform>-<python_version>.pyz


Documentation
-------------

See the `Docs on RTD`_ for examples and full documentation

.. _Docs on RTD: http://swimlane-python-driver.readthedocs.io/


Functional Tests
----------------

To run the Functional Tests, start by navigating into the *functional_tests* directory.

Install the required PIP packages with the command

::

    pip install -r requirements.txt


## Executing

The test suite allows for overriding the target server and user parameters via the following arguments:
 ::
    pytest 
    --url default="https://localhost"
    --user default="admin"
    --pass This is the password for the user defined above.
    --skipverify This is for allowing the version of PyDriver to not match the version of Swimlane.

To run a specific test and skip the version verification:

::
    pytest driver_tests/test_app_adaptor.py --skipverify

To run all the tests against 10.20.30.40:
 ::
    pytest --url "https://10.20.30.40"

.. NOTE::
    All of the data created for testing purposes is cleaned up.

    No preset data is needed beyond the base user.

    These tests are Python 3.6+ compatible.

Issues
------

Open any bug reports or feature requests through the `Swimlane support portal`_

.. _Swimlane support portal: https://support.swimlane.com/helpdesk/tickets/new
