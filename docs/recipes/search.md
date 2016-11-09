# Search
Swimlane uses reports to kick off searches. Searching with StatsReports will get you a generator that yields stat information.

```python
from swimlane.core.search import Search, groupby
from swimlane.core.resources import App, StatsReport

APP_ID = "567490ad55d95d5c30d02266"
USER_ID = "5674909d55d95d5c30d02200"

app = App.find(app_id=APP_ID)
field_id = app.field_id("Some Field Name")
```

## Reports

Swimlane supports two kinds of reports, Reports and StatsReports. Similarly to Record instances, you need to create prefilled instances of either of these types before sending them to Swimlane.

All examples below use Report but StatsReport have identical methods and can be used accordingly.

```python
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
from swimlane.core.search.aggregate import create_aggregate, AVG
report.aggregates = [create_aggregate(field_id, AVG)]
```

### Create new StatsReport
```python
stats_report = StatsReport.new_for(APP_ID, USER_ID, "A Stats Report")
stats_report.groupBys = [groupby.create_groupby(field_id, groupby.HOUR)]
result = Search(stats_report).execute()
result.stats # This is the generator that yields stats
Searching with a Report has a bit more options on the SearchResult that you get back from Search - but the main option is to paginate the results.

from swimlane.core.search import Search, filtering
from swimlane.core.resources import App, Report

APP_ID = "567490ad55d95d5c30d02266"
USER_ID = "5674909d55d95d5c30d02200"

app = App.find(app_id=APP_ID)
field_id = app.field_id("Some Field Name")
```


### Create New Report
```python
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
```
