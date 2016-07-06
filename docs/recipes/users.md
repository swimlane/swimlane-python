# Users & Groups

## Users
```python
from swimlane.core.resources import User

# Get a generator of all users in the system
all_users = User.find_all()

# Find a user by ID
user = User.find(user_id="5674909d55d95d5c30d02200")

# Get a generator of all users who's names match
users = User.find(name="samspade")
```

## Groups

```python
from swimlane.core.resources import Group

# Get a generator of all groups in the system
all_groups = Group.find_all()

# Get a group by ID
group = Group.find(group_id="568496a855d95f26400864bb")

# Get a generator of all groups who's names match
groups = Group.find(name="Private Eyes")
```
