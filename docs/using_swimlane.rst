##############
Using swimlane
##############


**********************
Connecting to Swimlane
**********************

The easiest way to connect to your Swimlane server is to set up a default
connection:

.. code-block:: python
  
  from swimlane.core.auth import Client

  Client.set_default("https://swimlane-server/", "username", "password")

This connection will be used for all communication with the Swimlane server for
as long as the Swimlane library remains in memory. This means that you can set
up your connection in a single, startup location and not worry about it from
then on.

****
Apps
****

Apps are central to Swimlane and to working with all other resources in ``swimlane``.

.. code-block:: python
  
  from swimlane.core.resources import App

  # Get a generator of all apps in the system
  all_apps = App.find_all()

  # Find an app by ID
  app = App.find(app_id="567490ad55d95d5c30d02266")

  # Find an app by name
  app = App.find(name="Incident Response")

  # Find an app by acronym
  app = App.find(acronym="IR")

  # Get the ID of a field for an app
  field_id = app.field_id("First Name")

*****
Users
*****

.. code-block:: python

  from swimlane.core.resources import User

  # Get a generator of all users in the system
  all_users = User.find_all()

  # Find a user by ID
  user = User.find(user_id="5674909d55d95d5c30d02200")

  # Get a generator of all users who's names match
  users = User.find(name="samspade")

******
Groups
******

.. code-block:: python

  from swimlane.core.resources import Group

  # Get a generator of all groups in the system
  all_groups = Group.find_all()

  # Get a group by ID
  group = Group.find(group_id="568496a855d95f26400864bb")

  # Get a generator of all groups who's names match
  groups = Group.find(name="Private Eyes")

*******
Records
*******

Records can be created directly from within this package. However, there are 
many fields that need to be prefilled.

.. code-block:: python

  from swimlane.core.resources import App, Record

  APP_ID = "567490ad55d95d5c30d02266"

  # Get a prefilled record
  record = Record.new_for(APP_ID)

  # Find a record by ID
  record = Record.find(APP_ID, "567490e955d95d5c30d022bf")

  # Insert a new record
  record = Record.new_for(APP_ID)
  app = App.find(app_id=APP_ID)
  field_id = app.field_id("Some Field Name")
  record.values[field_id] = "Some new value"
  record.insert()

  # Update a record
  record.values[field_id] = "An even newer value"
  record.update()
  
  # Update a Values List field in a record
  app = App.find(app_id=APP_ID)
  field_id = app.field_id("Colors")
  field_def = app.fields[field_id]
  value = field_def.values[0] # list of value defs
  record.values[field_id] = value.id # single select
  # record.values[field_id] = [value.id] # multi-select
  record.update()

  # Add a comment to a record
  user_id = "5674909d55d95d5c30d02200"
  record.add_comment(field_id, user_id, "Some comment")

  # Get references
  remote_rec_id = "568825d555d95d2a005f2f11"
  remote_field_id = "56881c1c848714d8b6d70683"
  record = Record.find(APP_ID, rec_id)
  refs = record.references(field_id, [remote_rec_id], [remote_field_id])

*****
Tasks
*****

It is possible to initiate a background Task in Swimlane. Once you have started
the task, you will need to go into Swimlane itself to see the results.

.. code-block:: python

  from swimlane.core.resources import Task

  # Get a generator of all tasks in the system
  tasks = Task.find_all()

  # Find a task by name
  task = Task.find(name="Reboot server at addr in field 1")

  # Run a task
  task.run(record=SOME_RECORD)

************************
Reports and StatsReports
************************

Swimlane supports two kinds of reports, ``Reports`` and ``StatsReports``.
Similarly to ``Record`` instances, you need to create prefilled instances
of eithe of these types before sending them to Swimlane.

All examples below use ``Report`` but ``StatsReport`` have identical methods
and can be used accordingly.

.. code-block:: python

  from swimlane.core.resources import Report, StatsReport

  APP_ID = "567490ad55d95d5c30d02266"
  USER_ID = "5674909d55d95d5c30d02200"

  # Find reports by ID
  report = Report.find("5686d8f755d95d19bcd60664")

  # Get a generator of all reports in the system
  all_reports = Report.find_all()

  # Get a prefilled record
  report = Report.new_for(APP_ID, USER_ID, "New Report")

  # Insert the report
  report.insert()

  # Update the report
  report.name = "New Report 123"
  report.update()

  # Add a filter to a report
  from swimlane.core.resources import App
  from swimlane.core.search.filtering import create_filter, EQ

  app = App.find(app_id=APP_ID)
  field_id = app.field_id("Some Field Name")
  report.filters = [create_filter(field_id, EQ, "blarg")]

  # Add grouping to a report
  from swimlane.core.search.groupby import create_groupby, HOUR
  report.groupBys = [create_groupby(field_id, HOUR)]

  # Add aggregation to a report
  from swimlane.core.search.aggregates import create_aggregate, AVG
  report.aggregates = [create_aggregate(field_id, AVG)]

*********
Searching
*********

Swimlane uses reports to kick off searches. Searching with ``StatsReports``
will get you a generator that yields stat information.

.. code-block:: python
 
  from swimlane.core.search import Search, groupby
  from swimlane.core.resources import App, StatsReport

  APP_ID = "567490ad55d95d5c30d02266"
  USER_ID = "5674909d55d95d5c30d02200"

  app = App.find(app_id=APP_ID)
  field_id = app.field_id("Some Field Name")

  # Create a new StatsReport
  stats_report = StatsReport.new_for(APP_ID, USER_ID, "A Stats Report")
  stats_report.groupBys = [groupby.create_groupby(field_id, groupby.HOUR)]
  result = Search(report).execute()
  result.stats # This is the generator that yeilds stats

Searching with a ``Report`` has a bit more options on the ``SearchResult``
that you get back from ``Search`` - but the main option is to paginate the
results.

.. code-block:: python

  from swimlane.core.search import Search, filtering
  from swimlane.core.resources import App, Report
  
  APP_ID = "567490ad55d95d5c30d02266"
  USER_ID = "5674909d55d95d5c30d02200"

  app = App.find(app_id=APP_ID)
  field_id = app.field_id("Some Field Name")

  # Create a new Report
  report = Report.new_for(APP_ID, USER_ID, "A Report")
  report.columns = [field_id]
  report.pageSize = 10
  report.filters = [filtering.create_filter(field_id, filtering.CONTAINS, "a")]

  search = Search(report)
  result = search.execute()
  result.count # The total number of records matched
  result.offset # The current page index of the search

  result.records # A generator that yields the Records for this page.

  # Use this pattern to iterate through all the results in the entire search
  while search.has_more_pages:
    result = search.next_page()
    result.records # A new generator for the current page.

