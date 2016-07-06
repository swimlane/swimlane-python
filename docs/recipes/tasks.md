# Tasks
It is possible to initiate a background Task in Swimlane. Once you have started the task, you will need to go into Swimlane itself to see the results.

```python
from swimlane.core.resources import Task

# Get a generator of all tasks in the system
tasks = Task.find_all()

# Find a task by name
task = Task.find(name="Reboot server at addr in field 1")

# Run a task
task.run(record=SOME_RECORD)
```
