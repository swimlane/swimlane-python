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
.. image:: https://api.codacy.com/project/badge/Grade/215d8281290749bba687a08db1d59d8b
    :target: https://www.codacy.com/app/Swimlane/swimlane-python?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=swimlane/swimlane-python&amp;utm_campaign=Badge_Grade
.. image:: https://api.codacy.com/project/badge/Coverage/215d8281290749bba687a08db1d59d8b
    :target: https://www.codacy.com/app/Swimlane/swimlane-python?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=swimlane/swimlane-python&amp;utm_campaign=Badge_Grade

Python driver for the Swimlane_ API

.. _Swimlane: http://swimlane.com


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

The tests take the following arguments\

--url   The url to a running Swimlane Instance. The default is *https://localhost*
--user  This is a user to run the tests as. The user needs Administrator privileges. The default is *admin*
--pass  This is the password for the user provided.
--skipverify    This is for allowing the version of PyDriver to not match the version of Swimlane.

.. NOTE::
    All of the data created for testing purposes is cleaned up.

    No preset data is needed beyond the base user.

    These tests are Python 2 and 3 compatible.

Issues
------

Open any bug reports or feature requests through the `Swimlane support portal`_

.. _Swimlane support portal: https://support.swimlane.com/helpdesk/tickets/new
