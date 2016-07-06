# Apps

Apps are central to Swimlane and to working with all other resources in swimlane.

```python
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
```
