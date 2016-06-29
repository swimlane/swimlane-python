"""Provides an App class."""

from ..auth import Client
from .resource import Resource


class App(Resource):
    """A simple abstraction over a Swimlane app."""

    def __init__(self, fields):
        """Init an App with fields.

        Args:
            fields (dict): A dict of fields and values
        """
        super(App, self).__init__(fields)

    def field_id(self, name):
        """Get the field ID of a field by name.

        Args:
            name (str): The name of the field.

        Returns:
            A field ID as a str.
        """
        return next((f["id"] for f in self.fields if f["name"] == name), None)

    def save(self):
        """Create/update the app."""
        if hasattr(self, 'id') and self.id:
            self._fields = Client.put(self, 'app/{}'.format(self.id))
        else:
            self._fields = Client.post(self, 'app')

    @classmethod
    def find_all(cls):
        """List all apps.

        Returns:
            A generator that yields all apps in the system.
        """
        return (App(x) for x in Client.get("apps/"))

    @classmethod
    def find(cls, app_id=None, name=None, acronym=None):
        """Find an application.

        Args:
            app_id (str): The app ID
            name (str): The app name
            acronym (str): The app acronym

        Returns:
            A resource that matches the fields
        """
        if app_id:
            return App(Client.get("app/{0}".format(app_id)))

        return next(
            (a for a in cls.find_all()
             if a.name == name or a.acronym == acronym), None)
