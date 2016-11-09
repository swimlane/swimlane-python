# Records
Records can be created directly from within this package. However, there are many fields that need to be pre-filled.

### Lookup & Update Record
```python
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

# Add a comment to a record
user_id = "5674909d55d95d5c30d02200"
record.add_comment(field_id, user_id, "Some comment")

# Get references
remote_rec_id = "568825d555d95d2a005f2f11"
remote_field_id = "56881c1c848714d8b6d70683"
record = Record.find(APP_ID, rec_id)
refs = record.references(field_id, [remote_rec_id], [remote_field_id])
```

### Add References
Use the following function to add references to one or more records from one App into a field on a record in another App by searching with keywords:

```python
from swimlane.records import add_references

refs = add_references(
    # The ID of the record where the refs will be stored
    record_id="5670dcec0e23ab0e4c363e12",
    # The keywords for searching. Any records that match these keywords will
    # be added as references and returned from this function.
    keywords="chisrv7008",
    #  You specify the app by passing app_id or app_name.
    app_name="Standard Operation",
    # specify remote app by passing remote_app_id or remote_app_name.
    remote_app_name="Common incidents",
    # The name of the field on record_id that will hold the references. You
    # can also specify this field by passing field_id.
    field_name="References"
)

for ref in refs: # This is a list of the records that were added as references.
    print refs
```
