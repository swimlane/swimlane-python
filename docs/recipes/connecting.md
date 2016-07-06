# Connecting to Swimlane
The easiest way to connect to your Swimlane server is to set up a default connection:

```python
from swimlane.core.auth import Client

Client.set_default("https://swimlane-server/", "username", "password")
```

This connection will be used for all communication with the Swimlane server for as long as the Swimlane library remains in memory. This means that you can set up your connection in a single, startup location and not worry about it from then on.
