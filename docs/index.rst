.. Swimlane Python documentation master file, created by
   sphinx-quickstart on Tue Jun  6 10:20:12 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Swimlane Python v\ |version|
============================

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

https://github.com/swimlane/swimlane-python

Python driver for the Swimlane_ API

.. _Swimlane: https://swimlane.com

Viewing docs for release v\ |release|

------------




Installation
------------


Pip
^^^

Recommended installation method is to install via `pip`.

Install latest release::

    pip install swimlane

Install latest release for platform v2.x::

    pip install 'swimlane>=2,<3'


Releases
^^^^^^^^

Manually clone_, checkout, and install specific release::

    git clone https://github.com/swimlane/swimlane-python
    cd swimlane-python
    git checkout <release>
    python setup.py install

.. _clone: https://github.com/swimlane/swimlane-python

Alternatively, download directly from `releases page`_, extract archive, and run same install command.

.. _releases page: https://github.com/swimlane/swimlane-python/releases


Versioning
^^^^^^^^^^

The Swimlane driver is versioned along with server, and will support all minor versions below installed version.
The latest major release should always be installed matching the target server version.

Newer minor server releases will typically work as expected, but could have minor inconsistencies or missing features.
A warning message will be logged when connecting to a newer minor server release than the current driver release, but
will otherwise work as expected.

.. warning::

    Major versions of driver and server are incompatible, and will **NOT** work together and will raise
    :class:`swimlane.exceptions.InvalidServerVersion` when attempting to connect.

For example, `swimlane==2.15.0` will fully support platform versions 2.0.0 - 2.15.0, will warn and attempt to work when
connecting to platform 2.15.1 - 2.x.y, and will fail when connecting to platform 3.0.0+.




Usage
-----

All connection and interaction with Swimlane API is handled via the :class:`swimlane.Swimlane` client.

Connection, authentication, and any additional requests will all be handled by the client class automatically throughout
the rest of the examples in the documentation.

Quick Start
^^^^^^^^^^^

.. code-block:: python

    from swimlane import Swimlane


    # Connect Swimlane client
    swimlane = Swimlane('https://192.168.1.1', 'username', 'password')


    # Retrieve App by name
    app = swimlane.apps.get(name='Target App')


    # Create new Record
    new_record = app.records.create(**{
        'Text Field': 'String',
        'Numeric Field': 100,
        'UserGroup Field': swimlane.user,
        'ValuesList Field': ['Option 1', 'Option 2']
    })


    # Work with field values
    assert new_record['Text Field'] == 'String'

    new_record['Numeric Field'] += 100
    assert new_record['Numeric Field'] == 200

    assert new_record['UserGroup Field'].id == swimlane.user.id


Examples
^^^^^^^^

Complete examples and descriptions of all driver functionality


.. toctree::

    examples/client
    examples/resources
    examples/fields




Package Docs
------------

Full API documentation for all package components

.. toctree::
    :titlesonly:

    apidoc/swimlane
