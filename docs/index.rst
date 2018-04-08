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

Install/upgrade to latest release::

    pip install -U swimlane

Install/upgrade to latest release for platform v2.x::

    pip install -U "swimlane>=2,<3"


Offline Installer
^^^^^^^^^^^^^^^^^

An installer including bundled dependencies is made available for easy offline installs

Download and run .pyz self-extracting archive from `Github releases page`_ for the correct platform and python version::

    wget https://github.com/swimlane/swimlane-python/releases/download/<release>/swimlane-python-<version>-offline-installer-<platform>-<python>.pyz
    python ./swimlane-python-<version>-offline-installer-<platform>-<python>.pyz

.. _Github releases page: https://github.com/swimlane/swimlane-python/releases

.. note::

    Offline installer requires pip v9+, installation will fail when attempting to use an earlier version. Verify pip
    version with `pip -V`.


Git
^^^

Manually clone from `Github repository`_, checkout, and install specific branch or release::

    git clone https://github.com/swimlane/swimlane-python
    cd swimlane-python
    git checkout <branch>
    pip install .

.. _Github repository: https://github.com/swimlane/swimlane-python

.. note::

    Installing via Git will install as a working version, and should only be used for driver development. Some features
    like server/client version compatibility checking may not work as expected when not installing production releases.


Versioning
^^^^^^^^^^

The Swimlane python driver is versioned along with the **Swimlane product version**, and will support
all minor versions below installed version. The latest major release should always be installed matching the target
server major build version. Patch version is reserved for driver fixes, and is not related to Swimlane server version.

Newer minor server releases will typically work as expected, but could have minor inconsistencies or missing features.
A warning message will be logged when connecting to a newer minor server release than the current driver release, but
will otherwise work as expected.

.. warning::

    Major versions of driver and server are incompatible, and will **NOT** work together and will raise
    :class:`swimlane.exceptions.InvalidServerVersion` when attempting to connect.

For example, `swimlane==2.15.0` will fully support Swimlane versions 2.0 - 2.15, will warn and attempt to work when
connecting to versions 2.16 - 2.x, and will fail when connecting to versions 3.0+.




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
